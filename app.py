"""Smart Crop Recommendation application entry point."""

import os
import sys
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

navigation = st.navigation([
    st.Page("pages/1_Home.py", title="Home", icon="🏡", default=True),
    st.Page("pages/2_Crop_Recommendation.py", title="Get a recommendation", icon="🌱"),
])
navigation.run()
