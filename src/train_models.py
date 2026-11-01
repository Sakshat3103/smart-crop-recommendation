"""
Training Script for Smart Crop Recommendation System.
Trains 5 machine learning classifiers, validates without data leakage,
computes evaluation metrics, selects the best model, and serializes artifacts.
"""

import os
import sys
import json
import joblib
import pandas as pd
from typing import Dict, Any

# Ensure matplotlib cache is in a writable location
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from src.data_preprocessing import load_crop_data, split_crop_data, FEATURE_NAMES
from src.evaluate_models import evaluate_single_model, compare_all_models


# Model configurations
MODEL_CONFIGS = {
    "random_forest": {
        "display_name": "Random Forest Classifier",
        "pipeline": Pipeline([
            ("classifier", RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42))
        ]),
        "desc": "Ensemble of decorrelated decision trees using bagging and feature subspace sampling for high accuracy and robustness."
    },
    "decision_tree": {
        "display_name": "Decision Tree Classifier",
        "pipeline": Pipeline([
            ("classifier", DecisionTreeClassifier(criterion="gini", max_depth=None, random_state=42))
        ]),
        "desc": "Non-parametric hierarchical decision tree that creates orthogonal decision boundaries based on feature entropy."
    },
    "knn": {
        "display_name": "K-Nearest Neighbors (KNN)",
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", KNeighborsClassifier(n_neighbors=5, weights="distance", metric="minkowski"))
        ]),
        "desc": "Distance-based instance learner that classifies points based on majority voting of standardized nearest neighbors."
    },
    "naive_bayes": {
        "display_name": "Gaussian Naive Bayes",
        "pipeline": Pipeline([
            ("classifier", GaussianNB())
        ]),
        "desc": "Probabilistic model assuming conditionally independent Gaussian distributions per feature given the crop class."
    },
    "svm": {
        "display_name": "Support Vector Machine (SVM)",
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", SVC(kernel="rbf", C=10.0, gamma="scale", probability=True, random_state=42))
        ]),
        "desc": "Kernel-based maximum margin classifier projecting standardized features into high-dimensional Hilbert space."
    }
}


def train_and_evaluate_all(data_path: str, models_dir: str) -> Dict[str, Any]:
    """
    Train all 5 models, evaluate them, serialize models and metrics.
    
    Args:
        data_path: Path to dataset CSV.
        models_dir: Directory where models and metrics will be saved.
        
    Returns:
        Dictionary of evaluation results.
    """
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"[*] Loading dataset from: {data_path}")
    df = load_crop_data(data_path)
    print(f"[+] Loaded {len(df)} records with {len(df.columns)} columns across {df['label'].nunique()} crop classes.")
    
    print("[*] Splitting dataset into stratified train (80%) and test (20%) sets...")
    X_train, X_test, y_train, y_test = split_crop_data(df, test_size=0.2, random_state=42)
    print(f"[+] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")
    
    # Preprocessor scaler artifact fit on training features only
    scaler = StandardScaler()
    scaler.fit(X_train)
    scaler_path = os.path.join(models_dir, "preprocessor.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"[+] Saved standalone preprocessor scaler to {scaler_path}")
    
    results = {}
    trained_pipelines = {}
    
    print("\n" + "="*70)
    print("TRAINING AND EVALUATING 5 CLASSIFICATION ALGORITHMS")
    print("="*70)
    
    for key, cfg in MODEL_CONFIGS.items():
        name = cfg["display_name"]
        pipeline = cfg["pipeline"]
        print(f"\n[*] Training {name}...")
        
        # Train
        pipeline.fit(X_train, y_train)
        trained_pipelines[key] = pipeline
        
        # Evaluate
        metrics = evaluate_single_model(pipeline, X_train, y_train, X_test, y_test, cv_folds=5)
        metrics["display_name"] = name
        metrics["description"] = cfg["desc"]
        results[key] = metrics
        
        # Save model pipeline
        model_file = os.path.join(models_dir, f"{key}.pkl")
        joblib.dump(pipeline, model_file)
        
        print(f"    - Accuracy  : {metrics['accuracy'] * 100:.2f}%")
        print(f"    - F1-Score  : {metrics['f1_score'] * 100:.2f}%")
        print(f"    - Precision : {metrics['precision'] * 100:.2f}%")
        print(f"    - Recall    : {metrics['recall'] * 100:.2f}%")
        print(f"    - CV Mean   : {metrics['cv_mean'] * 100:.2f}% (±{metrics['cv_std'] * 100:.2f}%)")
        print(f"    - Saved to  : {model_file}")

    # Determine best model based on F1-score, then accuracy
    best_key = max(results.keys(), key=lambda k: (results[k]["f1_score"], results[k]["accuracy"]))
    best_name = results[best_key]["display_name"]
    best_pipeline = trained_pipelines[best_key]
    
    best_path = os.path.join(models_dir, "best_model.pkl")
    joblib.dump(best_pipeline, best_path)
    print(f"\n[🏆] Best Performing Model: {best_name} (F1: {results[best_key]['f1_score']*100:.2f}%)")
    print(f"[+] Serialized best model to {best_path}")
    
    # Save overall metrics summary to JSON
    summary_data = {
        "best_model_key": best_key,
        "best_model_name": best_name,
        "feature_names": FEATURE_NAMES,
        "classes": results[best_key]["classes"],
        "models": {
            k: {
                "display_name": v["display_name"],
                "description": v["description"],
                "accuracy": v["accuracy"],
                "precision": v["precision"],
                "recall": v["recall"],
                "f1_score": v["f1_score"],
                "cv_mean": v["cv_mean"],
                "cv_std": v["cv_std"],
                "confusion_matrix": v["confusion_matrix"],
                "classification_report": v["classification_report"]
            }
            for k, v in results.items()
        }
    }
    
    metrics_path = os.path.join(models_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"[+] Saved evaluation metrics to {metrics_path}")
    
    # Display comparison table
    comp_dict = {cfg["display_name"]: results[k] for k, cfg in MODEL_CONFIGS.items()}
    df_comp = compare_all_models(comp_dict)
    print("\n" + "="*70)
    print("MODEL COMPARISON SUMMARY")
    print("="*70)
    print(df_comp.to_string(index=False))
    print("="*70)
    
    return summary_data


if __name__ == "__main__":
    default_data = os.path.join(PROJECT_ROOT, "data", "crop_recommendation.csv")
    default_models = os.path.join(PROJECT_ROOT, "models")
    train_and_evaluate_all(default_data, default_models)
