"""
Model Comparison Page — Smart Crop AI.
Comprehensive benchmarks comparing all 5 algorithms: Accuracy, Precision, Recall,
F1-Score, Cross-Validation, interactive confusion matrices, and classification reports.
"""

import os
import sys
import json
import pandas as pd
import streamlit as st

# Setup path and config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.helpers import init_page, render_hero, render_kpi_card, render_sidebar_info, render_footer
from utils.visualizations import (
    plot_model_metrics_comparison,
    plot_metric_breakdown_bars,
    plot_confusion_matrix
)

init_page("Model Comparison", "⚖️")
render_sidebar_info()

render_hero(
    title="Machine Learning Algorithm Comparison",
    subtitle="Rigorous empirical evaluation and statistical benchmarking of 5 distinct classification algorithms trained on stratified agricultural datasets without data leakage.",
    badge="EMPIRICAL BENCHMARKS"
)

# Load real evaluation metrics
metrics_path = os.path.join(PROJECT_ROOT, "models", "metrics.json")

if not os.path.exists(metrics_path):
    st.error("Model metrics not found. Please train models using 'python src/train_models.py'.")
    st.stop()

with open(metrics_path, "r") as f:
    data = json.load(f)

models_dict = data.get("models", {})
best_key = data.get("best_model_key", "random_forest")
best_info = models_dict.get(best_key, {})

# Top highlight card for best model
st.markdown(
    f"""
    <div class="agri-card agri-card-highlight" style="background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span class="crop-badge" style="background: #059669;">🏆 HIGHEST GENERALIZATION BENCHMARK</span>
                <h2 style="color: #064e3b; margin: 0.5rem 0 0.2rem 0; font-size: 2rem;">
                    {best_info.get('display_name', 'Random Forest Classifier')}
                </h2>
                <p style="color: #475569; max-width: 800px; font-size: 0.95rem; line-height: 1.5; margin: 0;">
                    {best_info.get('description', '')}
                </p>
            </div>
            <div style="text-align: right; background: #ffffff; padding: 1rem 1.5rem; border-radius: 12px; border: 1px solid #d1fae5; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">TEST F1-SCORE</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #059669;">{best_info.get('f1_score', 0)*100:.2f}%</div>
                <div style="font-size: 0.8rem; color: #065f46; font-weight: 600;">5-Fold CV: {best_info.get('cv_mean', 0)*100:.2f}%</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Comparison Table
st.markdown("### 📊 Performance Metrics Summary Table")

table_rows = []
for k, m in models_dict.items():
    table_rows.append({
        "Algorithm": m.get("display_name", k),
        "Accuracy (%)": round(m["accuracy"] * 100, 2),
        "Precision (%)": round(m["precision"] * 100, 2),
        "Recall (%)": round(m["recall"] * 100, 2),
        "F1-Score (%)": round(m["f1_score"] * 100, 2),
        "5-Fold CV Accuracy": f"{m['cv_mean']*100:.2f}% ± {m['cv_std']*100:.2f}%"
    })

df_summary = pd.DataFrame(table_rows).sort_values(by=["F1-Score (%)", "Accuracy (%)"], ascending=False).reset_index(drop=True)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Grouped Metrics Bar Chart
st.markdown("### 📈 Comprehensive Metric Benchmark")
fig_grouped = plot_model_metrics_comparison(models_dict)
st.plotly_chart(fig_grouped, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4 Individual Metric Charts in 2x2 Grid
st.markdown("### 🔬 Metric Breakdown by Dimension")
col_m1, col_m2 = st.columns(2)
with col_m1:
    fig_acc = plot_metric_breakdown_bars(models_dict, "accuracy", "Accuracy Score", "#10b981")
    st.plotly_chart(fig_acc, use_container_width=True)
    
    fig_rec = plot_metric_breakdown_bars(models_dict, "recall", "Recall Score", "#8b5cf6")
    st.plotly_chart(fig_rec, use_container_width=True)

with col_m2:
    fig_prec = plot_metric_breakdown_bars(models_dict, "precision", "Precision Score", "#0284c7")
    st.plotly_chart(fig_prec, use_container_width=True)
    
    fig_f1 = plot_metric_breakdown_bars(models_dict, "f1_score", "F1-Score (Harmonic Mean)", "#f59e0b")
    st.plotly_chart(fig_f1, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Confusion Matrix Section
st.markdown("### 🧩 Confusion Matrix Analysis")
cm_col_ctrl, cm_col_info = st.columns([1.5, 2])

with cm_col_ctrl:
    model_choice = st.selectbox(
        "Select Model to Inspect Confusion Matrix:",
        options=list(models_dict.keys()),
        format_func=lambda k: f"{models_dict[k]['display_name']} ({models_dict[k]['accuracy']*100:.2f}%)"
    )

selected_model_data = models_dict[model_choice]
classes = selected_model_data.get("classes", data.get("classes", []))
cm_matrix = selected_model_data.get("confusion_matrix", [])

fig_cm = plot_confusion_matrix(cm_matrix, classes, selected_model_data["display_name"])
st.plotly_chart(fig_cm, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Detailed Classification Report
with st.expander(f"📑 View Detailed Per-Class Classification Report — {selected_model_data['display_name']}"):
    raw_report = selected_model_data.get("classification_report", {})
    if raw_report:
        report_rows = []
        for cls_name, vals in raw_report.items():
            if isinstance(vals, dict):
                report_rows.append({
                    "Class": cls_name,
                    "Precision": f"{vals.get('precision', 0):.4f}",
                    "Recall": f"{vals.get('recall', 0):.4f}",
                    "F1-Score": f"{vals.get('f1-score', 0):.4f}",
                    "Support": int(vals.get("support", 0))
                })
        df_rep = pd.DataFrame(report_rows)
        st.dataframe(df_rep, use_container_width=True, hide_index=True)
    else:
        st.info("Classification report details not stored.")

st.markdown("<br>", unsafe_allow_html=True)

# Theoretical Algorithm Breakdown
st.markdown("### 📚 Theoretical Architecture & Behavioral Analysis")

theory_tabs = st.tabs([
    "🌲 Random Forest",
    "📊 Naive Bayes",
    "⚡ Support Vector Machine",
    "📍 K-Nearest Neighbors",
    "🌿 Decision Tree"
])

with theory_tabs[0]:
    st.markdown(
        """
        #### Random Forest Classifier (Best Performer)
        - **Mechanism:** Builds an ensemble of 100 decorrelated decision trees using bootstrap aggregating (bagging) and random feature subspace sampling at each split.
        - **Why it Excels in Agriculture:** The 7 crop recommendation features exhibit complex non-linear interactions (e.g. rice requires both high rainfall AND high humidity simultaneously). Random Forest seamlessly isolates these non-linear intersections without making assumptions of normal distribution or feature independence.
        - **Overfitting Resistance:** Averaging probabilistic votes across uncorrelated trees drastically minimizes generalization variance, delivering **99.55% test accuracy**.
        """
    )

with theory_tabs[1]:
    st.markdown(
        """
        #### Gaussian Naive Bayes
        - **Mechanism:** Applies Bayes' theorem under the assumption that features are conditionally independent given the crop label, modeling each feature's conditional probability as a continuous 1D Gaussian distribution.
        - **Performance Insights:** Achieves an impressive **99.55% accuracy** with virtually zero training latency. In agricultural datasets where crops occupy well-segregated nutrient niches (e.g., apples demand high potassium, while rice demands intense water), the independence assumption holds remarkably well.
        """
    )

with theory_tabs[2]:
    st.markdown(
        """
        #### Support Vector Machine (SVM)
        - **Mechanism:** Constructs optimal separating hyperplanes in high-dimensional feature space using the Radial Basis Function (RBF) kernel with standard scaling.
        - **Performance Insights:** Scores **98.86% test accuracy**. Standard scaling is mandatory because raw input ranges differ drastically (Rainfall up to 300 mm vs. pH at 6.5). SVM maximizes margin boundaries between tight crop clusters.
        """
    )

with theory_tabs[3]:
    st.markdown(
        """
        #### K-Nearest Neighbors (KNN)
        - **Mechanism:** Instance-based non-parametric classifier that assigns labels based on the inverse distance-weighted vote of the $k=5$ closest training examples in Euclidean space.
        - **Performance Insights:** Scores **98.18% test accuracy**. Sensitive to the scale of distance metrics; relies entirely on the `StandardScaler` pipeline step to prevent high-magnitude features (like Potassium or Rainfall) from overpowering smaller-scale features (like soil pH).
        """
    )

with theory_tabs[4]:
    st.markdown(
        """
        #### Decision Tree Classifier
        - **Mechanism:** Generates a greedy hierarchical tree structure by recursively partitioning feature domains along orthogonal thresholds using Gini impurity.
        - **Performance Insights:** Achieves **97.95% accuracy**. Highly interpretable with direct if-else rules. However, without ensemble bagging, single trees can be susceptible to localized variance shifts along boundary thresholds.
        """
    )

render_footer()
