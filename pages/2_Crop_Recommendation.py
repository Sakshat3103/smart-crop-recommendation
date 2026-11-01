"""Farmer-facing crop recommendation page."""

import os
import sys
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_preprocessing import FEATURE_CONSTRAINTS, FEATURE_NAMES
from src.predict_crop import CropPredictor
from utils.crop_information import get_crop_profile
from utils.visualizations import plot_prediction_confidence_gauge
from utils.helpers import add_to_history, get_history_df, init_page, render_footer, render_hero, render_kpi_card, render_sidebar_info

init_page("Crop Recommendation", "🌱")
render_sidebar_info()
render_hero(
    title="Crop Recommendation",
    subtitle="Add your farm conditions to receive a crop suggestion and practical growing guidance.",
    badge="FARM ADVISORY",
)

predictor = CropPredictor()
PRESETS = {
    "Enter my own values": None,
    "Rice / Paddy — humid, high-rainfall conditions": {"N": 90.0, "P": 42.0, "K": 43.0, "temperature": 21.0, "humidity": 82.0, "ph": 6.5, "rainfall": 203.0},
    "Maize — moderate rainfall conditions": {"N": 80.0, "P": 48.0, "K": 20.0, "temperature": 23.0, "humidity": 65.0, "ph": 6.3, "rainfall": 68.0},
    "Cotton — warm conditions": {"N": 118.0, "P": 46.0, "K": 19.0, "temperature": 24.0, "humidity": 80.0, "ph": 6.9, "rainfall": 80.0},
}

top_left, top_right = st.columns([2, 1])
with top_left:
    selected_preset = st.selectbox("Use an example field condition (optional)", list(PRESETS))
with top_right:
    st.write("&nbsp;", unsafe_allow_html=True)
    if st.button("Reset values", use_container_width=True):
        st.session_state.input_values = {"N": 50.0, "P": 50.0, "K": 50.0, "temperature": 25.0, "humidity": 70.0, "ph": 6.5, "rainfall": 100.0}
        st.session_state.last_prediction = None
        st.rerun()
if PRESETS[selected_preset]:
    st.session_state.input_values.update(PRESETS[selected_preset])

st.markdown("### Enter your farm conditions")
soil_col, weather_col = st.columns(2)

def input_slider(feature, step):
    config = FEATURE_CONSTRAINTS[feature]
    value = st.slider(
        f"{config['label']} ({config['unit']})",
        min_value=float(config["min"]), max_value=float(config["max"]),
        value=float(st.session_state.input_values.get(feature, config["default"])), step=step,
        help=config["desc"],
    )
    st.session_state.input_values[feature] = value

with soil_col:
    st.markdown("#### 🌱 Soil details")
    st.caption("Use soil-test values where available.")
    input_slider("N", 1.0)
    input_slider("P", 1.0)
    input_slider("K", 1.0)
    input_slider("ph", 0.1)
with weather_col:
    st.markdown("#### ⛅ Local weather")
    st.caption("Use typical conditions for the coming growing season.")
    input_slider("temperature", 0.5)
    input_slider("humidity", 1.0)
    input_slider("rainfall", 1.0)

recommend = st.button("🌱 Recommend a Crop", type="primary", use_container_width=True)
if recommend or st.session_state.get("last_prediction"):
    farm_inputs = {name: float(st.session_state.input_values[name]) for name in FEATURE_NAMES}
    with st.spinner("Preparing your crop recommendation..."):
        result = predictor.predict(farm_inputs, model_key="best_model", top_k_alternatives=3)
    if not result["success"]:
        st.error("Please review the values entered for your farm.")
        for error in result.get("errors", []):
            st.warning(error)
    else:
        if recommend:
            add_to_history(result)
        crop_name = result["recommended_crop"]
        crop = get_crop_profile(crop_name) or {}
        alternatives = result.get("alternatives", [])
        st.markdown("---")
        st.markdown("## Your crop recommendation")
        result_col, match_col = st.columns([1.6, 1])
        with result_col:
            st.markdown(f"""<div class="recommendation-hero"><div style="font-size: 3.5rem;">{crop.get('icon', '🌱')}</div><div class="crop-result-title">{crop_name.title()}</div><p style="color: #334155; max-width: 560px; margin: 0 auto; line-height: 1.55;">{crop.get('description', 'This crop is a suitable match for the conditions entered.')}</p></div>""", unsafe_allow_html=True)
        with match_col:
            if result.get("confidence") is not None:
                st.plotly_chart(plot_prediction_confidence_gauge(result["confidence"], crop_name), use_container_width=True)
            if alternatives:
                st.markdown("#### Other crops to consider")
                for alternative in alternatives:
                    alt_crop = get_crop_profile(alternative["crop"]) or {}
                    st.markdown(f"- {alt_crop.get('icon', '🌱')} **{alternative['crop'].title()}** — {alternative['probability']:.0f}% match")
        st.markdown("### Growing guidance")
        for column, title, value, desc, icon in zip(
            st.columns(4), ["Temperature", "Humidity", "Soil pH", "Rainfall"],
            [crop.get("ideal_temp_range", "Varies"), crop.get("ideal_humidity_range", "Varies"), crop.get("suitable_ph_range", "Varies"), crop.get("rainfall_requirement", "Varies")],
            ["Suitable growing range", "Suitable growing range", "Suitable soil condition", "Seasonal water need"], ["🌡️", "💧", "🧪", "🌧️"],
        ):
            with column:
                render_kpi_card(title, value, desc, icon)
        guidance_left, guidance_right = st.columns(2)
        with guidance_left:
            soils = "".join(f"<li>{soil}</li>" for soil in crop.get("soil_types", [])) or "<li>Consult a local soil specialist.</li>"
            st.markdown(f"""<div class="agri-card"><h4>🌱 Season and soil</h4><p><strong>Best season:</strong> {crop.get('season', 'Varies by location')}</p><p><strong>Crop duration:</strong> {crop.get('growth_duration', 'Varies')}</p><p><strong>Suitable soils:</strong></p><ul>{soils}</ul></div>""", unsafe_allow_html=True)
        with guidance_right:
            practices = "".join(f"<li>{practice}</li>" for practice in crop.get("cultivation_practices", [])) or "<li>Follow guidance from your local agricultural extension office.</li>"
            st.markdown(f"""<div class="agri-card"><h4>🚜 Practical cultivation tips</h4><ul>{practices}</ul></div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Recommendations in this visit")
history = get_history_df()
if history.empty:
    st.caption("Your recommendations will appear here during this visit.")
else:
    visible_columns = [column for column in ["Timestamp", "Recommended Crop", "Confidence (%)"] if column in history.columns]
    st.dataframe(history[visible_columns], use_container_width=True, hide_index=True)
    if st.button("Clear recommendations from this visit"):
        st.session_state.prediction_history = []
        st.session_state.last_prediction = None
        st.rerun()

render_footer()
