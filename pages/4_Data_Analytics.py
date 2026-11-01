"""
Data Analytics Dashboard — Smart Crop AI.
Interactive exploratory data analysis, parametric distributions, correlation matrices,
crop class balancing, and multi-variable relationship visualizations.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Setup path and config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_preprocessing import load_crop_data, get_dataset_summary, FEATURE_NAMES, FEATURE_CONSTRAINTS
from utils.helpers import init_page, render_hero, render_kpi_card, render_sidebar_info, render_footer
from utils.visualizations import (
    plot_crop_class_distribution,
    plot_correlation_heatmap,
    plot_feature_distribution,
    plot_feature_by_crop_comparison
)

init_page("Data Analytics Dashboard", "📊")
render_sidebar_info()

render_hero(
    title="Agricultural Data Analytics Dashboard",
    subtitle="Interactive exploratory data analysis revealing soil nutrient distributions, environmental ranges, parametric correlations, and crop class characteristics.",
    badge="EXPLORATORY DATA ANALYSIS"
)

# Load real dataset
data_path = os.path.join(PROJECT_ROOT, "data", "crop_recommendation.csv")
if not os.path.exists(data_path):
    st.error("Dataset not found at data/crop_recommendation.csv.")
    st.stop()

df = load_crop_data(data_path)
summary = get_dataset_summary(df)
overview = summary["overview"]

# Dataset KPI Metrics
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    render_kpi_card("Total Records", f"{overview['total_records']:,}", "Agricultural samples", "📋")
with c2:
    render_kpi_card("Total Features", overview["num_features"], "Physical parameters", "🧪")
with c3:
    render_kpi_card("Crop Classes", overview["num_classes"], "Unique target crops", "🌾")
with c4:
    render_kpi_card("Missing Values", overview["missing_values"], "Zero null cells", "✅")
with c5:
    render_kpi_card("Duplicates", overview["duplicate_records"], "Zero duplicate rows", "🛡️")

st.markdown("<br>", unsafe_allow_html=True)

# Dataset Preview & Summary Statistics Expander
with st.expander("🔍 View Raw Dataset Preview & Statistical Description", expanded=False):
    tab_data, tab_stats = st.tabs(["📄 Sample Data Records", "📐 Descriptive Statistics"])
    with tab_data:
        st.dataframe(df.head(15), use_container_width=True)
        st.caption(f"Showing top 15 of {len(df)} records.")
    with tab_stats:
        st.dataframe(df.describe().T, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Class Distribution & Correlation Matrix Row
st.markdown("### 🌾 Crop Class Distribution & Feature Correlations")
col_dist, col_corr = st.columns([1.3, 1.7])

with col_dist:
    fig_class = plot_crop_class_distribution(df)
    st.plotly_chart(fig_class, use_container_width=True)
    st.caption("The dataset features a perfectly balanced distribution of exactly 100 samples per crop class.")

with col_corr:
    fig_corr = plot_correlation_heatmap(df, FEATURE_NAMES)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("Pearson correlation reveals strong positive correlation between Phosphorus (P) and Potassium (K) (r = 0.74).")

st.markdown("<br>", unsafe_allow_html=True)

# Parametric Distributions Section (Individual Features)
st.markdown("### 🔬 Soil Nutrient & Climate Parameter Distributions")

selected_feature = st.selectbox(
    "Select Parameter to Inspect Distribution:",
    options=FEATURE_NAMES,
    format_func=lambda f: f"{FEATURE_CONSTRAINTS[f]['label']} ({FEATURE_CONSTRAINTS[f]['unit']})"
)

f_cfg = FEATURE_CONSTRAINTS[selected_feature]
dist_col1, dist_col2 = st.columns([2, 1])

with dist_col1:
    fig_dist = plot_feature_distribution(df, selected_feature, f_cfg["label"], f_cfg["unit"])
    st.plotly_chart(fig_dist, use_container_width=True)

with dist_col2:
    feat_series = df[selected_feature]
    st.markdown(
        f"""
        <div class="agri-card" style="height: 100%;">
            <h4 style="color: #064e3b; margin-top: 0;">Statistical Overview</h4>
            <p style="font-size: 0.9rem; color: #475569;">{f_cfg['desc']}</p>
            <hr style="border-color: #f1f5f9; margin: 0.8rem 0;">
            <table style="width: 100%; font-size: 0.88rem;">
                <tr><td style="color: #64748b;">Mean:</td><td style="font-weight: 700; text-align: right;">{feat_series.mean():.2f} {f_cfg['unit']}</td></tr>
                <tr><td style="color: #64748b;">Std Dev:</td><td style="font-weight: 700; text-align: right;">{feat_series.std():.2f} {f_cfg['unit']}</td></tr>
                <tr><td style="color: #64748b;">Minimum:</td><td style="font-weight: 700; text-align: right;">{feat_series.min():.2f} {f_cfg['unit']}</td></tr>
                <tr><td style="color: #64748b;">Median (Q2):</td><td style="font-weight: 700; text-align: right;">{feat_series.median():.2f} {f_cfg['unit']}</td></tr>
                <tr><td style="color: #64748b;">Maximum:</td><td style="font-weight: 700; text-align: right;">{feat_series.max():.2f} {f_cfg['unit']}</td></tr>
                <tr><td style="color: #64748b;">IQR:</td><td style="font-weight: 700; text-align: right;">{feat_series.quantile(0.75) - feat_series.quantile(0.25):.2f} {f_cfg['unit']}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Feature Relationships with Crop Classes (Interactive Filters)
st.markdown("### 🚜 Crop-Specific Nutrient & Environmental Demands")

ctrl_c1, ctrl_c2 = st.columns([1.5, 2])
with ctrl_c1:
    crop_filter_feature = st.selectbox(
        "Select Parameter to Compare Across Crops:",
        options=FEATURE_NAMES,
        index=6,  # Default to rainfall
        format_func=lambda f: f"{FEATURE_CONSTRAINTS[f]['label']} ({FEATURE_CONSTRAINTS[f]['unit']})"
    )

with ctrl_c2:
    all_crops = sorted(df["label"].unique().tolist())
    selected_crops = st.multiselect(
        "Filter Specific Crops (Leave blank for all 22):",
        options=all_crops,
        default=["rice", "maize", "chickpea", "apple", "cotton", "coffee", "watermelon"]
    )

fig_crops = plot_feature_by_crop_comparison(
    df,
    feature=crop_filter_feature,
    feature_label=FEATURE_CONSTRAINTS[crop_filter_feature]["label"],
    unit=FEATURE_CONSTRAINTS[crop_filter_feature]["unit"],
    selected_crops=selected_crops if selected_crops else None
)
st.plotly_chart(fig_crops, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Multi-dimensional Bivariate Scatter Plot with Crop Coloring
st.markdown("### 🌐 Bivariate Feature Interaction Explorer")
biv_c1, biv_c2, biv_c3 = st.columns(3)

with biv_c1:
    x_axis = st.selectbox("X-Axis Feature:", options=FEATURE_NAMES, index=0)
with biv_c2:
    y_axis = st.selectbox("Y-Axis Feature:", options=FEATURE_NAMES, index=1)
with biv_c3:
    highlight_crop = st.multiselect(
        "Crops to Highlight on Scatter:",
        options=all_crops,
        default=["rice", "apple", "banana", "cotton", "chickpea"]
    )

scatter_df = df[df["label"].isin(highlight_crop)] if highlight_crop else df

import plotly.express as px
fig_scatter = px.scatter(
    scatter_df,
    x=x_axis,
    y=y_axis,
    color="label",
    title=f"<b>Bivariate Clustering: {FEATURE_CONSTRAINTS[x_axis]['label']} vs. {FEATURE_CONSTRAINTS[y_axis]['label']}</b>",
    labels={
        x_axis: f"{FEATURE_CONSTRAINTS[x_axis]['label']} ({FEATURE_CONSTRAINTS[x_axis]['unit']})",
        y_axis: f"{FEATURE_CONSTRAINTS[y_axis]['label']} ({FEATURE_CONSTRAINTS[y_axis]['unit']})",
        "label": "Crop Class"
    },
    template="plotly_white",
    hover_data=FEATURE_NAMES
)
fig_scatter.update_layout(
    margin={"l": 40, "r": 30, "t": 40, "b": 40},
    legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5}
)
st.plotly_chart(fig_scatter, use_container_width=True)

render_footer()
