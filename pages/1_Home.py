"""Farmer-facing home page for Smart Crop Recommendation."""

import os
import sys
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.helpers import init_page, render_hero, render_kpi_card, render_sidebar_info, render_footer

init_page("Home", "🌱")
render_sidebar_info()
render_hero(
    title="Find the Right Crop for Your Farm",
    subtitle="Enter your soil test results and local weather conditions to receive a practical crop recommendation and growing guidance.",
    badge="FARM ADVISORY",
)

st.markdown("### Make a confident planting decision")
intro, action = st.columns([2, 1])
with intro:
    st.markdown("""<div class="agri-card agri-card-highlight"><h3 style="color: #064e3b; margin-top: 0;">🌾 Guidance based on your field conditions</h3><p style="color: #334155; line-height: 1.65; margin-bottom: 0;">Use the recommendation tool with your soil nutrient values, soil pH, temperature, humidity, and expected rainfall. You will receive a suggested crop, suitable alternatives, and practical cultivation guidance.</p></div>""", unsafe_allow_html=True)
with action:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🌱 Get a Crop Recommendation", type="primary", use_container_width=True):
        st.switch_page("pages/2_Crop_Recommendation.py")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### How it works")
for column, icon, title, text in zip(
    st.columns(3),
    ["🧪", "🌱", "🚜"],
    ["1. Enter field details", "2. Get a recommendation", "3. Plan the season"],
    ["Add soil-test values and local weather conditions.", "Receive a crop suggestion tailored to those conditions.", "Review suitable soil, season, water, and cultivation guidance."],
):
    with column:
        st.markdown(f"""<div class="agri-card" style="text-align: center; height: 100%;"><div style="font-size: 2.2rem;">{icon}</div><h4 style="color: #064e3b; margin: 0.6rem 0 0.4rem;">{title}</h4><p style="color: #475569; font-size: 0.9rem; margin-bottom: 0;">{text}</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### What you will need")
for column, title, value, desc, icon in zip(
    st.columns(4),
    ["Soil nutrients", "Soil condition", "Local weather", "Water conditions"],
    ["N · P · K", "pH", "Temperature", "Rainfall"],
    ["From a soil test, if available", "Acidity or alkalinity", "Typical growing-season conditions", "Expected rainfall for the season"],
    ["🌱", "🧪", "🌡️", "🌧️"],
):
    with column:
        render_kpi_card(title, value, desc, icon)

st.info("For best results, use recent soil-test and local weather information. This tool supports crop planning and should be used alongside local agricultural advice.")
render_footer()
