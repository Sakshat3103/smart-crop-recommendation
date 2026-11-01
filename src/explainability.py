"""
Explainable AI (XAI) Module for Crop Recommendation.
Provides global feature importance (Random Forest, Decision Tree) and local feature
attributions using SHAP (SHapley Additive exPlanations) and sensitivity analysis.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

# Ensure matplotlib config directory is writable
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import shap
from src.data_preprocessing import FEATURE_NAMES, FEATURE_CONSTRAINTS


class CropExplainer:
    """
    Explainability engine for crop recommendation models.
    """
    
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            models_dir = os.path.join(PROJECT_ROOT, "models")
        self.models_dir = models_dir
        self._rf_pipeline = None
        self._dt_pipeline = None
        self._shap_explainer = None
        
    def _get_rf_pipeline(self):
        if self._rf_pipeline is None:
            path = os.path.join(self.models_dir, "random_forest.pkl")
            if not os.path.exists(path):
                raise FileNotFoundError(f"Random Forest model not found at '{path}'.")
            self._rf_pipeline = joblib.load(path)
        return self._rf_pipeline

    def _get_dt_pipeline(self):
        if self._dt_pipeline is None:
            path = os.path.join(self.models_dir, "decision_tree.pkl")
            if not os.path.exists(path):
                raise FileNotFoundError(f"Decision Tree model not found at '{path}'.")
            self._dt_pipeline = joblib.load(path)
        return self._dt_pipeline

    def _get_shap_explainer(self):
        if self._shap_explainer is None:
            rf = self._get_rf_pipeline().named_steps["classifier"]
            self._shap_explainer = shap.TreeExplainer(rf)
        return self._shap_explainer

    def get_global_feature_importance(self, model_type: str = "random_forest") -> pd.DataFrame:
        """
        Extract global feature importance from tree-based ensemble models.
        
        Args:
            model_type: 'random_forest' or 'decision_tree'
            
        Returns:
            DataFrame with Feature, Importance, and Percentage columns sorted descending.
        """
        if model_type == "decision_tree":
            pipeline = self._get_dt_pipeline()
            title = "Decision Tree"
        else:
            pipeline = self._get_rf_pipeline()
            title = "Random Forest"
            
        classifier = pipeline.named_steps["classifier"]
        importances = classifier.feature_importances_
        
        df_imp = pd.DataFrame({
            "Feature": FEATURE_NAMES,
            "Feature_Label": [FEATURE_CONSTRAINTS[f]["label"] for f in FEATURE_NAMES],
            "Importance": importances,
            "Percentage": (importances / np.sum(importances)) * 100
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
        
        return df_imp

    def explain_instance_shap(
        self, 
        inputs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Compute local SHAP attribution values for a specific set of input features.
        
        Args:
            inputs: Dictionary containing 7 input parameters.
            
        Returns:
            Dictionary containing predicted crop, base values, SHAP values per feature,
            and natural language explanation.
        """
        pipeline = self._get_rf_pipeline()
        explainer = self._get_shap_explainer()
        
        # Build DataFrame with single row
        input_df = pd.DataFrame([{col: float(inputs[col]) for col in FEATURE_NAMES}])
        
        # Inference
        pred_crop = pipeline.predict(input_df)[0]
        classes = list(pipeline.classes_)
        pred_idx = classes.index(pred_crop)
        
        # Compute SHAP values
        shap_values = explainer.shap_values(input_df)
        
        # Extract values for the target predicted class
        if isinstance(shap_values, list):
            feature_shap = shap_values[pred_idx][0]
        elif hasattr(shap_values, "values") and shap_values.values.ndim == 3:
            feature_shap = shap_values.values[0, :, pred_idx]
        elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
            if shap_values.shape[2] == len(classes):
                feature_shap = shap_values[0, :, pred_idx]
            else:
                feature_shap = shap_values[pred_idx, 0, :]
        else:
            feature_shap = np.array(shap_values[0])
            
        # Expected value (base rate probability)
        expected_val = explainer.expected_value
        if isinstance(expected_val, (list, np.ndarray)):
            base_val = float(expected_val[pred_idx])
        else:
            base_val = float(expected_val)
            
        # Structure explanations
        contributions = []
        for feat, val, shap_val in zip(FEATURE_NAMES, input_df.iloc[0], feature_shap):
            impact_direction = "Positive (Favored)" if shap_val > 0 else "Negative (Dissuaded)"
            contributions.append({
                "feature": feat,
                "label": FEATURE_CONSTRAINTS[feat]["label"],
                "value": float(val),
                "unit": FEATURE_CONSTRAINTS[feat]["unit"],
                "shap_value": round(float(shap_val), 4),
                "abs_shap": round(abs(float(shap_val)), 4),
                "impact": impact_direction
            })
            
        # Sort by absolute SHAP value (magnitude of influence)
        contributions = sorted(contributions, key=lambda x: x["abs_shap"], reverse=True)
        
        # Formulate human-readable summary
        top_positive = [c for c in contributions if c["shap_value"] > 0][:3]
        top_negative = [c for c in contributions if c["shap_value"] < 0][:2]
        
        pos_str = ", ".join([f"{c['label']} ({c['value']} {c['unit']})" for c in top_positive]) if top_positive else "None"
        neg_str = ", ".join([f"{c['label']} ({c['value']} {c['unit']})" for c in top_negative]) if top_negative else "None"
        
        text_explanation = (
            f"The Random Forest model recommended **{pred_crop.title()}** primarily driven by favorable "
            f"levels of {pos_str}."
        )
        if top_negative:
            text_explanation += f" Conversely, conditions such as {neg_str} slightly restricted confidence."
            
        return {
            "predicted_crop": pred_crop,
            "base_value": base_val,
            "contributions": contributions,
            "top_positive": top_positive,
            "top_negative": top_negative,
            "summary_text": text_explanation,
            "disclaimer": (
                "Notice: Feature attributions quantify the internal mathematical weights and splits "
                "assigned by the trained model pipeline. While informative, they represent statistical "
                "patterns in training data rather than biological causal laws."
            )
        }

    def analyze_parameter_sensitivity(
        self, 
        base_inputs: Dict[str, float], 
        variation_pct: float = 0.20
    ) -> List[Dict[str, Any]]:
        """
        Simulate how ±variation_pct shifts in individual parameters alter the recommendation.
        
        Args:
            base_inputs: Current baseline values.
            variation_pct: Fraction to test upwards and downwards (e.g. 0.20 = 20%).
            
        Returns:
            List of sensitivity outcomes per parameter.
        """
        pipeline = self._get_rf_pipeline()
        base_df = pd.DataFrame([{col: float(base_inputs[col]) for col in FEATURE_NAMES}])
        base_pred = pipeline.predict(base_df)[0]
        
        sensitivity_results = []
        for feat in FEATURE_NAMES:
            bounds = FEATURE_CONSTRAINTS[feat]
            val = float(base_inputs[feat])
            delta = max((bounds["max"] - bounds["min"]) * variation_pct, 1.0)
            
            # Lower variant
            low_val = max(bounds["min"], val - delta)
            low_df = base_df.copy()
            low_df.at[0, feat] = low_val
            low_pred = pipeline.predict(low_df)[0]
            
            # Higher variant
            high_val = min(bounds["max"], val + delta)
            high_df = base_df.copy()
            high_df.at[0, feat] = high_val
            high_pred = pipeline.predict(high_df)[0]
            
            stability = "Stable" if (low_pred == base_pred and high_pred == base_pred) else "Sensitive"
            
            sensitivity_results.append({
                "feature": feat,
                "label": bounds["label"],
                "unit": bounds["unit"],
                "current_val": val,
                "decreased_val": round(low_val, 2),
                "decreased_pred": low_pred,
                "increased_val": round(high_val, 2),
                "increased_pred": high_pred,
                "stability": stability
            })
            
        return sensitivity_results
