"""
Evaluation Module for Machine Learning Models.
Computes accuracy, precision, recall, f1-score, cross-validation metrics,
confusion matrices, and per-class classification reports.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import StratifiedKFold, cross_val_score


def evaluate_single_model(
    model: Any, 
    X_train: pd.DataFrame, 
    y_train: pd.Series, 
    X_test: pd.DataFrame, 
    y_test: pd.Series,
    cv_folds: int = 5
) -> Dict[str, Any]:
    """
    Evaluate a fitted model or pipeline on test data and compute cross-validation.
    
    Args:
        model: Trained scikit-learn estimator or Pipeline.
        X_train: Training features.
        y_train: Training labels.
        X_test: Testing features.
        y_test: Testing labels.
        cv_folds: Number of stratified folds for cross-validation.
        
    Returns:
        Dictionary containing all evaluation metrics.
    """
    # Test set predictions
    y_pred = model.predict(X_test)
    
    # Calculate weighted metrics
    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    recall = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
    
    # Stratified K-Fold Cross-Validation on training data to verify generalization
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring="accuracy")
    
    # Confusion matrix
    classes = sorted(list(y_test.unique()))
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    
    # Detailed classification report
    report_dict = classification_report(y_test, y_pred, labels=classes, output_dict=True, zero_division=0)
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "cv_mean": float(np.mean(cv_scores)),
        "cv_std": float(np.std(cv_scores)),
        "confusion_matrix": cm.tolist(),
        "classes": classes,
        "classification_report": report_dict
    }


def compare_all_models(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Format model comparison results into a structured summary DataFrame.
    
    Args:
        results: Dictionary mapping model names to evaluation result dictionaries.
        
    Returns:
        Pandas DataFrame sorted by F1-score and Accuracy descending.
    """
    rows = []
    for name, m in results.items():
        rows.append({
            "Algorithm": name,
            "Accuracy": round(m["accuracy"], 4),
            "Precision": round(m["precision"], 4),
            "Recall": round(m["recall"], 4),
            "F1-Score": round(m["f1_score"], 4),
            "CV Accuracy (Mean ± Std)": f"{m['cv_mean'] * 100:.2f}% ± {m['cv_std'] * 100:.2f}%"
        })
    df_compare = pd.DataFrame(rows)
    df_compare = df_compare.sort_values(by=["F1-Score", "Accuracy"], ascending=False).reset_index(drop=True)
    return df_compare
