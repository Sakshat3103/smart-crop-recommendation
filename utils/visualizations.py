"""
Visualization Utilities for Smart Crop AI.
Creates modern, interactive, and responsive Plotly charts adhering to the
green and modern agri-tech design aesthetic.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Palette definitions
AGRI_PALETTE = {
    "primary": "#10b981",       # Emerald
    "primary_dark": "#065f46",  # Deep forest green
    "primary_light": "#d1fae5", # Pale mint
    "secondary": "#0284c7",     # Fresh blue
    "accent": "#f59e0b",        # Amber
    "danger": "#ef4444",        # Red
    "background": "#ffffff",
    "card_bg": "#f8fafc",
    "text": "#0f172a",
    "muted": "#64748b"
}

CHART_THEME = {
    "font": {"family": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif", "color": "#0f172a"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 40, "r": 30, "t": 40, "b": 40}
}


def plot_model_metrics_comparison(metrics_dict: Dict[str, Dict[str, Any]]) -> go.Figure:
    """
    Generate grouped interactive bar chart comparing Accuracy, Precision, Recall, and F1-Score.
    """
    models = []
    accs = []
    precs = []
    recs = []
    f1s = []
    
    for key, data in metrics_dict.items():
        models.append(data.get("display_name", key))
        accs.append(data["accuracy"] * 100)
        precs.append(data["precision"] * 100)
        recs.append(data["recall"] * 100)
        f1s.append(data["f1_score"] * 100)
        
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Accuracy", x=models, y=accs, marker_color="#10b981", text=[f"{v:.1f}%" for v in accs], textposition="auto"))
    fig.add_trace(go.Bar(name="Precision", x=models, y=precs, marker_color="#0284c7", text=[f"{v:.1f}%" for v in precs], textposition="auto"))
    fig.add_trace(go.Bar(name="Recall", x=models, y=recs, marker_color="#8b5cf6", text=[f"{v:.1f}%" for v in recs], textposition="auto"))
    fig.add_trace(go.Bar(name="F1-Score", x=models, y=f1s, marker_color="#f59e0b", text=[f"{v:.1f}%" for v in f1s], textposition="auto"))
    
    fig.update_layout(
        barmode="group",
        title="<b>Algorithm Performance Comparison (%)</b>",
        yaxis={"title": "Score (%)", "range": [90, 101], "gridcolor": "#e2e8f0"},
        xaxis={"title": "Machine Learning Model"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        **CHART_THEME
    )
    return fig


def plot_metric_breakdown_bars(metrics_dict: Dict[str, Dict[str, Any]], metric_key: str, metric_name: str, color: str) -> go.Figure:
    """
    Single metric comparison bar chart sorted descending.
    """
    items = []
    for k, d in metrics_dict.items():
        items.append({
            "Model": d.get("display_name", k),
            "Score": d[metric_key] * 100
        })
    df = pd.DataFrame(items).sort_values(by="Score", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=df["Score"],
        y=df["Model"],
        orientation="h",
        marker_color=color,
        text=[f"{v:.2f}%" for v in df["Score"]],
        textposition="outside"
    ))
    fig.update_layout(
        title=f"<b>{metric_name} Comparison</b>",
        xaxis={"title": f"{metric_name} (%)", "range": [90, 102], "gridcolor": "#e2e8f0"},
        yaxis={"title": ""},
        **CHART_THEME
    )
    return fig


def plot_confusion_matrix(cm_data: List[List[int]], classes: List[str], model_name: str = "Best Model") -> go.Figure:
    """
    Render 22x22 confusion matrix with interactive tooltips and green-toned colormap.
    """
    fig = px.imshow(
        cm_data,
        x=classes,
        y=classes,
        labels=dict(x="Predicted Crop", y="Actual Crop", color="Samples"),
        color_continuous_scale="Greens",
        aspect="auto"
    )
    fig.update_layout(
        title=f"<b>Confusion Matrix Heatmap — {model_name}</b>",
        xaxis={"tickangle": -45, "title": "Predicted Label"},
        yaxis={"title": "True Label"},
        **CHART_THEME
    )
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, feature_cols: List[str]) -> go.Figure:
    """
    Correlation heatmap for continuous soil and climatic parameters.
    """
    corr = df[feature_cols].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        labels=dict(color="Pearson Corr")
    )
    fig.update_layout(
        title="<b>Soil Nutrients & Climate Correlation Heatmap</b>",
        **CHART_THEME
    )
    return fig


def plot_feature_distribution(df: pd.DataFrame, feature: str, feature_label: str, unit: str) -> go.Figure:
    """
    Distribution histogram with marginal box plot for a single parameter.
    """
    fig = px.histogram(
        df,
        x=feature,
        nbins=40,
        marginal="box",
        color_discrete_sequence=["#10b981"],
        opacity=0.85
    )
    fig.update_layout(
        title=f"<b>Distribution of {feature_label} ({unit})</b>",
        xaxis={"title": f"{feature_label} ({unit})", "gridcolor": "#e2e8f0"},
        yaxis={"title": "Frequency", "gridcolor": "#e2e8f0"},
        **CHART_THEME
    )
    return fig


def plot_feature_by_crop_comparison(
    df: pd.DataFrame, 
    feature: str, 
    feature_label: str, 
    unit: str, 
    selected_crops: Optional[List[str]] = None
) -> go.Figure:
    """
    Boxplot showing how a soil or weather parameter differs across crops.
    """
    plot_df = df if not selected_crops else df[df["label"].isin(selected_crops)]
    fig = px.box(
        plot_df,
        x="label",
        y=feature,
        color="label",
        labels={"label": "Crop Class", feature: f"{feature_label} ({unit})"}
    )
    fig.update_layout(
        title=f"<b>{feature_label} Requirements by Crop Class</b>",
        xaxis={"tickangle": -45, "title": "Crop"},
        yaxis={"gridcolor": "#e2e8f0"},
        showlegend=False,
        **CHART_THEME
    )
    return fig


def plot_crop_class_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Class distribution bar chart demonstrating balanced nature of dataset.
    """
    counts = df["label"].value_counts().reset_index()
    counts.columns = ["Crop", "Count"]
    counts = counts.sort_values(by="Crop")
    
    fig = px.bar(
        counts,
        x="Crop",
        y="Count",
        color_discrete_sequence=["#065f46"],
        text="Count"
    )
    fig.update_layout(
        title="<b>Crop Class Distribution (Samples per Class)</b>",
        xaxis={"tickangle": -45, "title": "Crop Class"},
        yaxis={"title": "Number of Records", "range": [0, 120], "gridcolor": "#e2e8f0"},
        **CHART_THEME
    )
    return fig


def plot_global_feature_importance(df_imp: pd.DataFrame, title_prefix: str = "Random Forest") -> go.Figure:
    """
    Horizontal bar chart of Gini/impurity feature importance scores.
    """
    df_sorted = df_imp.sort_values(by="Importance", ascending=True)
    fig = go.Figure(go.Bar(
        x=df_sorted["Importance"],
        y=df_sorted["Feature_Label"],
        orientation="h",
        marker={"color": df_sorted["Importance"], "colorscale": "Teal"},
        text=[f"{p:.1f}%" for p in df_sorted["Percentage"]],
        textposition="outside"
    ))
    fig.update_layout(
        title=f"<b>Global Feature Importance ({title_prefix})</b>",
        xaxis={"title": "Relative Importance Score", "gridcolor": "#e2e8f0"},
        yaxis={"title": ""},
        **CHART_THEME
    )
    return fig


def plot_shap_waterfall_bars(contributions: List[Dict[str, Any]], predicted_crop: str) -> go.Figure:
    """
    Waterfall / bidirectional bar chart illustrating positive and negative SHAP pushes.
    """
    df = pd.DataFrame(contributions).sort_values(by="shap_value", ascending=True)
    colors = ["#10b981" if v >= 0 else "#ef4444" for v in df["shap_value"]]
    
    fig = go.Figure(go.Bar(
        x=df["shap_value"],
        y=df["label"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.4f}" for v in df["shap_value"]],
        textposition="outside"
    ))
    fig.update_layout(
        title=f"<b>SHAP Feature Attribution Towards '{predicted_crop.title()}'</b>",
        xaxis={"title": "SHAP Value (Contribution to Log-Odds / Class Probability)", "gridcolor": "#e2e8f0"},
        yaxis={"title": "Environmental Feature"},
        **CHART_THEME
    )
    return fig


def plot_prediction_confidence_gauge(confidence: float, crop_name: str) -> go.Figure:
    """
    Sleek speedometer / indicator gauge for model confidence score.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        number={"suffix": "%", "font": {"size": 36, "color": "#065f46"}},
        title={"text": f"<b>Confidence for {crop_name.title()}</b>", "font": {"size": 18, "color": "#0f172a"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": "#10b981"},
            "bgcolor": "#f1f5f9",
            "borderwidth": 1,
            "bordercolor": "#cbd5e1",
            "steps": [
                {"range": [0, 50], "color": "#fee2e2"},
                {"range": [50, 75], "color": "#fef3c7"},
                {"range": [75, 100], "color": "#d1fae5"}
            ],
            "threshold": {
                "line": {"color": "#065f46", "width": 4},
                "thickness": 0.8,
                "value": confidence
            }
        }
    ))
    fig.update_layout(
        height=260,
        margin={"l": 25, "r": 25, "t": 35, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"}
    )
    return fig


def plot_user_radar_comparison(user_inputs: Dict[str, float], crop_mean_profile: Dict[str, float]) -> go.Figure:
    """
    Radar chart comparing user's environmental input against typical optimal conditions for the crop.
    Values are normalized 0-100 for visual comparison.
    """
    # Max scales for normalization
    scales = {
        "N": 140.0, "P": 145.0, "K": 205.0,
        "temperature": 45.0, "humidity": 100.0,
        "ph": 10.0, "rainfall": 300.0
    }
    
    categories = ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Temperature", "Humidity", "Soil pH", "Rainfall"]
    keys = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    
    user_norm = [(user_inputs.get(k, 0) / scales[k]) * 100 for k in keys]
    crop_norm = [(crop_mean_profile.get(k, 0) / scales[k]) * 100 for k in keys]
    
    # Close polygon
    categories.append(categories[0])
    user_norm.append(user_norm[0])
    crop_norm.append(crop_norm[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=user_norm,
        theta=categories,
        fill="toself",
        name="Your Inputs",
        line_color="#10b981",
        fillcolor="rgba(16, 185, 129, 0.25)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=crop_norm,
        theta=categories,
        fill="toself",
        name="Crop Optimal Benchmark",
        line_color="#0284c7",
        fillcolor="rgba(2, 132, 199, 0.2)"
    ))
    
    fig.update_layout(
        polar={
            "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "#e2e8f0"}
        },
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
        title="<b>Input Conditions vs. Crop Benchmark (Normalized %)</b>",
        **CHART_THEME
    )
    return fig
