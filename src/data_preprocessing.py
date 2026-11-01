"""
Data Preprocessing Module for Smart Crop Recommendation System.
Handles dataset loading, validation, feature extraction, summary statistics,
and train-test splitting with stratification.
"""

import os
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Define standard feature names and target column
FEATURE_NAMES: List[str] = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_NAME: str = "label"

# Realistic agricultural boundaries based on the empirical dataset distribution
FEATURE_CONSTRAINTS: Dict[str, Dict[str, Any]] = {
    "N": {
        "min": 0.0,
        "max": 140.0,
        "unit": "kg/ha",
        "label": "Nitrogen (N)",
        "desc": "Ratio of Nitrogen content in soil",
        "default": 50.0
    },
    "P": {
        "min": 5.0,
        "max": 145.0,
        "unit": "kg/ha",
        "label": "Phosphorus (P)",
        "desc": "Ratio of Phosphorus content in soil",
        "default": 50.0
    },
    "K": {
        "min": 5.0,
        "max": 205.0,
        "unit": "kg/ha",
        "label": "Potassium (K)",
        "desc": "Ratio of Potassium content in soil",
        "default": 50.0
    },
    "temperature": {
        "min": 8.0,
        "max": 45.0,
        "unit": "°C",
        "label": "Temperature",
        "desc": "Ambient temperature in Celsius",
        "default": 25.0
    },
    "humidity": {
        "min": 10.0,
        "max": 100.0,
        "unit": "%",
        "label": "Relative Humidity",
        "desc": "Relative humidity percentage",
        "default": 70.0
    },
    "ph": {
        "min": 3.5,
        "max": 10.0,
        "unit": "pH scale",
        "label": "Soil pH",
        "desc": "Acidity / alkalinity value of the soil (0-14)",
        "default": 6.5
    },
    "rainfall": {
        "min": 20.0,
        "max": 300.0,
        "unit": "mm",
        "label": "Rainfall",
        "desc": "Total seasonal / annual rainfall in mm",
        "default": 100.0
    }
}


def load_crop_data(filepath: str) -> pd.DataFrame:
    """
    Load crop recommendation dataset from a CSV file.
    
    Args:
        filepath: Path to the CSV file.
        
    Returns:
        Pandas DataFrame containing the crop data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Crop dataset not found at '{filepath}'.")
    df = pd.read_csv(filepath)
    # Strip whitespace from columns if any
    df.columns = [c.strip() for c in df.columns]
    return df


def validate_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate the dataset structure, missing values, duplicates, and column types.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Dictionary containing validation results.
    """
    missing_cols = [col for col in FEATURE_NAMES + [TARGET_NAME] if col not in df.columns]
    null_counts = df.isnull().sum().to_dict()
    duplicate_count = int(df.duplicated().sum())
    
    is_valid = (len(missing_cols) == 0) and (sum(null_counts.values()) == 0)
    
    return {
        "is_valid": is_valid,
        "missing_columns": missing_cols,
        "null_counts": null_counts,
        "duplicate_count": duplicate_count,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "classes": sorted(df[TARGET_NAME].unique().tolist()) if TARGET_NAME in df.columns else []
    }


def get_dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute comprehensive summary statistics for the dataset.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Dictionary containing overview metrics, class balance, and feature summaries.
    """
    validation = validate_dataset(df)
    features_df = df[FEATURE_NAMES]
    
    stats_dict = features_df.describe().to_dict()
    class_counts = df[TARGET_NAME].value_counts().to_dict()
    
    return {
        "overview": {
            "total_records": len(df),
            "num_features": len(FEATURE_NAMES),
            "num_classes": len(class_counts),
            "duplicate_records": validation["duplicate_count"],
            "missing_values": sum(validation["null_counts"].values())
        },
        "feature_stats": stats_dict,
        "class_distribution": class_counts,
        "classes": sorted(list(class_counts.keys()))
    }


def split_crop_data(
    df: pd.DataFrame, 
    test_size: float = 0.2, 
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset into stratified training and testing sets.
    
    Args:
        df: Input DataFrame.
        test_size: Fraction of data for testing.
        random_state: Reproducibility seed.
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    X = df[FEATURE_NAMES].copy()
    y = df[TARGET_NAME].copy()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=y
    )
    return X_train, X_test, y_train, y_test


def validate_user_input(inputs: Dict[str, float]) -> Tuple[bool, List[str]]:
    """
    Validate user inputs against agricultural physical constraints.
    
    Args:
        inputs: Dictionary of feature names and user input values.
        
    Returns:
        Tuple of (is_valid: bool, list_of_error_messages)
    """
    errors: List[str] = []
    for feature, bounds in FEATURE_CONSTRAINTS.items():
        if feature not in inputs:
            errors.append(f"Missing required parameter '{bounds['label']}'.")
            continue
        try:
            val = float(inputs[feature])
            if np.isnan(val):
                errors.append(f"'{bounds['label']}' cannot be empty or NaN.")
            elif val < bounds["min"] or val > bounds["max"]:
                errors.append(
                    f"'{bounds['label']}' value ({val} {bounds['unit']}) is out of permissible range "
                    f"[{bounds['min']} - {bounds['max']} {bounds['unit']}]."
                )
        except (ValueError, TypeError):
            errors.append(f"'{bounds['label']}' must be a valid numeric value.")
            
    return (len(errors) == 0, errors)
