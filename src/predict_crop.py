"""
Prediction Inference Engine for Smart Crop Recommendation.
Loads serialized models/pipelines, performs inference, calculates prediction confidence,
and determines alternative crop suggestions.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_preprocessing import FEATURE_NAMES, validate_user_input


class CropPredictor:
    """
    Inference wrapper for crop recommendation machine learning models.
    """
    
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            models_dir = os.path.join(PROJECT_ROOT, "models")
        self.models_dir = models_dir
        self._loaded_models: Dict[str, Any] = {}
        
    def load_model(self, model_key: str = "best_model") -> Any:
        """
        Load a trained model pipeline from disk with caching.
        
        Args:
            model_key: Identifier of the model (e.g., 'best_model', 'random_forest', 'svm', etc.)
            
        Returns:
            The loaded scikit-learn pipeline or estimator.
        """
        if model_key in self._loaded_models:
            return self._loaded_models[model_key]
            
        filename = f"{model_key}.pkl" if not model_key.endswith(".pkl") else model_key
        model_path = os.path.join(self.models_dir, filename)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Trained model artifact not found at '{model_path}'. Please train models first.")
            
        model = joblib.load(model_path)
        self._loaded_models[model_key] = model
        return model

    def predict(
        self, 
        inputs: Dict[str, float], 
        model_key: str = "best_model",
        top_k_alternatives: int = 3
    ) -> Dict[str, Any]:
        """
        Predict the most suitable crop and alternative crops given environmental inputs.
        
        Args:
            inputs: Dictionary containing all 7 environmental parameters:
                    N, P, K, temperature, humidity, ph, rainfall.
            model_key: Key of the model to use for prediction.
            top_k_alternatives: Number of alternative crop suggestions to return.
            
        Returns:
            Dictionary containing prediction outcome, confidence, alternatives, and metadata.
        """
        # Validate inputs
        is_valid, errors = validate_user_input(inputs)
        if not is_valid:
            return {
                "success": False,
                "errors": errors,
                "recommended_crop": None,
                "confidence": None,
                "alternatives": []
            }
            
        # Format input DataFrame matching training feature schema
        input_data = {col: [float(inputs[col])] for col in FEATURE_NAMES}
        input_df = pd.DataFrame(input_data)
        
        # Load model pipeline
        pipeline = self.load_model(model_key)
        
        # Primary prediction
        prediction = pipeline.predict(input_df)[0]
        
        # Confidence score and alternative recommendations
        confidence: Optional[float] = None
        alternatives: List[Dict[str, Any]] = []
        
        if hasattr(pipeline, "predict_proba"):
            try:
                probabilities = pipeline.predict_proba(input_df)[0]
                classes = pipeline.classes_
                prob_pairs = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)
                
                # Confidence of top prediction
                for cls_name, prob in prob_pairs:
                    if cls_name == prediction:
                        confidence = round(float(prob) * 100, 2)
                        break
                        
                # Top alternative candidates (excluding top 1)
                for cls_name, prob in prob_pairs[1:top_k_alternatives + 1]:
                    if prob > 0.001:  # Only meaningful probabilities
                        alternatives.append({
                            "crop": cls_name,
                            "probability": round(float(prob) * 100, 2)
                        })
            except Exception as e:
                # If predict_proba fails for any estimator configuration, fallback safely
                confidence = None
                alternatives = []
                
        return {
            "success": True,
            "recommended_crop": prediction,
            "confidence": confidence,
            "alternatives": alternatives,
            "model_used": model_key,
            "input_summary": {k: float(inputs[k]) for k in FEATURE_NAMES},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# Quick test helper
if __name__ == "__main__":
    predictor = CropPredictor()
    test_input = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 20.88, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9
    }
    result = predictor.predict(test_input)
    print("Prediction test result:", result)
