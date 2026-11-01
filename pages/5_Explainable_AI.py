"""
Explainable AI (XAI) Page — Smart Crop AI.
Global feature importances, local SHAP attribution waterfall charts,
decision explanations, and parameter sensitivity simulators.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Setup path and config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.explainability import CropExplainer
from src.data_preprocessing import FEATURE_NAMES, FEATURE_CONSTRAINTS
from utils.helpers import init_page, render_hero, render_kpi_card, render_sidebar_info, render_footer
from utils.visualizations import (
    plot_global_feature_importance,
    plot_shap_waterfall_bars
)

init_page("Explainable AI (XAI)", "🔍")
render_sidebar_info()

render_hero(
    title="Explainable AI (XAI) & Interpretability",
    subtitle="Demystifying complex machine learning models through global feature importances, local SHAP (SHapley Additive exPlanations) values, and parameter sensitivity testing.",
    badge="INTERPRETABLE MACHINE LEARNING"
)

explainer = CropExplainer()

# Global Feature Importance Section
st.markdown("### 🌐 Global Model Feature Importance")
st.markdown(
    """
    Global feature importance quantifies how much each soil and climate factor reduces impurity 
    across all 100 decision trees in the ensemble during training.
    """
)

imp_col_ctrl, imp_col_chart = st.columns([1, 2])
with imp_col_ctrl:
    tree_model_type = st.radio(
        "Select Model for Feature Importance:",
        options=["random_forest", "decision_tree"],
        format_func=lambda k: "Random Forest Classifier" if k == "random_forest" else "Decision Tree Classifier"
    )
    
    df_imp = explainer.get_global_feature_importance(tree_model_type)
    
    st.markdown(
        """
        <div class="agri-card" style="margin-top: 1rem;">
            <h4 style="color: #064e3b; margin-top: 0;">Key Takeaways</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                <strong>Rainfall</strong> and <strong>Relative Humidity</strong> emerge as the most decisive 
                macro-discriminators across crops, closely followed by soil <strong>Potassium (K)</strong> 
                and <strong>Phosphorus (P)</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with imp_col_chart:
    title_prefix = "Random Forest" if tree_model_type == "random_forest" else "Decision Tree"
    fig_imp = plot_global_feature_importance(df_imp, title_prefix=title_prefix)
    st.plotly_chart(fig_imp, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Local SHAP Attribution Explorer
st.markdown("### 🧩 Local Prediction Explainability with SHAP")
st.markdown(
    """
    SHAP computes the fair marginal contribution of each physical feature towards recommending a specific crop, 
    based on cooperative game theory. Positive values (green) push the model towards the recommendation, while 
    negative values (red) reduce confidence.
    """
)

# Test inputs
c_s1, c_s2, c_s3, c_s4 = st.columns(4)
with c_s1:
    x_n = st.number_input("Nitrogen (N)", min_value=0.0, max_value=140.0, value=float(st.session_state.input_values.get("N", 90.0)), step=5.0)
    x_temp = st.number_input("Temperature (°C)", min_value=8.0, max_value=45.0, value=float(st.session_state.input_values.get("temperature", 21.0)), step=1.0)
with c_s2:
    x_p = st.number_input("Phosphorus (P)", min_value=5.0, max_value=145.0, value=float(st.session_state.input_values.get("P", 42.0)), step=5.0)
    x_hum = st.number_input("Humidity (%)", min_value=10.0, max_value=100.0, value=float(st.session_state.input_values.get("humidity", 82.0)), step=5.0)
with c_s3:
    x_k = st.number_input("Potassium (K)", min_value=5.0, max_value=205.0, value=float(st.session_state.input_values.get("K", 43.0)), step=5.0)
    x_rain = st.number_input("Rainfall (mm)", min_value=20.0, max_value=300.0, value=float(st.session_state.input_values.get("rainfall", 203.0)), step=10.0)
with c_s4:
    x_ph = st.number_input("Soil pH", min_value=3.5, max_value=10.0, value=float(st.session_state.input_values.get("ph", 6.5)), step=0.2)
    st.write("&nbsp;")
    explain_btn = st.button("🔍 Explain This Prediction", use_container_width=True, type="primary")

test_features = {
    "N": x_n, "P": x_p, "K": x_k,
    "temperature": x_temp, "humidity": x_hum, "ph": x_ph, "rainfall": x_rain
}

with st.spinner("Computing SHAP attributions via TreeExplainer..."):
    shap_data = explainer.explain_instance_shap(test_features)

pred_crop = shap_data["predicted_crop"]

shap_col1, shap_col2 = st.columns([1.5, 1.5])
with shap_col1:
    fig_shap = plot_shap_waterfall_bars(shap_data["contributions"], pred_crop)
    st.plotly_chart(fig_shap, use_container_width=True)

with shap_col2:
    st.markdown(
        f"""
        <div class="agri-card" style="height: 100%;">
            <span class="crop-badge">PREDICTION TARGET: {pred_crop.upper()}</span>
            <h3 style="color: #064e3b; margin: 0.5rem 0;">Attribution Breakdown</h3>
            <p style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                {shap_data['summary_text']}
            </p>
            <h5 style="color: #064e3b; margin-top: 1rem;">Feature Contribution Details:</h5>
            <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #e2e8f0; font-weight: 600; color: #475569;">
                    <th style="text-align: left; padding: 4px;">Parameter</th>
                    <th style="text-align: right; padding: 4px;">Value</th>
                    <th style="text-align: right; padding: 4px;">SHAP</th>
                    <th style="text-align: right; padding: 4px;">Impact</th>
                </tr>
        """,
        unsafe_allow_html=True
    )
    for c in shap_data["contributions"]:
        impact_color = "#059669" if c["shap_value"] >= 0 else "#dc2626"
        st.markdown(
            f"""
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 4px; color: #1e293b;">{c['label']}</td>
                <td style="text-align: right; padding: 4px;">{c['value']} {c['unit']}</td>
                <td style="text-align: right; padding: 4px; font-weight: 600; color: {impact_color};">{c['shap_value']:+.4f}</td>
                <td style="text-align: right; padding: 4px; color: {impact_color};">{c['impact'].split()[0]}</td>
            </tr>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</table></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Parameter Sensitivity Analysis Simulator
st.markdown("### 🧪 Parameter Sensitivity & Environmental Shift Simulator")
st.markdown(
    """
    Test the stability of the recommendation: How does varying a single soil or climatic parameter by 
    **±20%** alter the recommended crop cultivar?
    """
)

sensitivity_results = explainer.analyze_parameter_sensitivity(test_features, variation_pct=0.20)

sens_rows = []
for s in sensitivity_results:
    sens_rows.append({
        "Environmental Parameter": s["label"],
        "Current Value": f"{s['current_val']} {s['unit']}",
        "Decreased (-20%)": f"{s['decreased_val']} {s['unit']}",
        "Prediction at -20%": s["decreased_pred"].title(),
        "Increased (+20%)": f"{s['increased_val']} {s['unit']}",
        "Prediction at +20%": s["increased_pred"].title(),
        "Model Stability": "🟢 Stable" if s["stability"] == "Stable" else "🟡 Boundary Sensitive"
    })

df_sens = pd.DataFrame(sens_rows)
st.dataframe(df_sens, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# Important Ethical & Scientific Caution
st.markdown(
    """
    <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 5px solid #f59e0b; padding: 1.2rem; border-radius: 8px;">
        <h4 style="color: #92400e; margin: 0 0 0.4rem 0;">⚠️ Scientific Disclaimer: Association vs. Causation</h4>
        <p style="color: #78350f; font-size: 0.9rem; line-height: 1.5; margin: 0;">
            Feature importance scores and SHAP attribution values quantify the internal mathematical weights and decision 
            thresholds learned by the model from the training dataset. <strong>They do NOT constitute proof of biological causation.</strong> 
            While agricultural parameters are strongly grounded in plant physiology, farmers and agronomists must consider 
            micro-drainage, local soil microbiological health, seed quality, and pest vectors before making critical sowing investments.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

render_footer()
