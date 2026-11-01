"""
UI Helpers, Layout Utilities, and Session State Management for Smart Crop AI.
"""

import os
import io
import pandas as pd
import streamlit as st
from typing import Dict, Any, List, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "style.css")


def load_css() -> str:
    """Load style.css content."""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r") as f:
            return f.read()
    return ""


def init_page(page_title: str, page_icon: str = "🌾") -> None:
    """
    Standardize Streamlit page configuration and inject modern styling.
    """
    st.set_page_config(
        page_title=f"{page_title} | Smart Crop AI",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject CSS
    css_content = load_css()
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        
    init_session_state()


def init_session_state() -> None:
    """
    Ensure all session state keys exist across pages.
    """
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []
    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None
    if "input_values" not in st.session_state:
        st.session_state.input_values = {
            "N": 50.0,
            "P": 50.0,
            "K": 50.0,
            "temperature": 25.0,
            "humidity": 70.0,
            "ph": 6.5,
            "rainfall": 100.0
        }


def add_to_history(result: Dict[str, Any]) -> None:
    """
    Save a prediction record into the session history.
    """
    if not result.get("success"):
        return
        
    record = {
        "Timestamp": result.get("timestamp"),
        "Recommended Crop": result.get("recommended_crop", "").title(),
        "Confidence (%)": result.get("confidence", "N/A"),
        "Nitrogen (N)": result.get("input_summary", {}).get("N"),
        "Phosphorus (P)": result.get("input_summary", {}).get("P"),
        "Potassium (K)": result.get("input_summary", {}).get("K"),
        "Temperature (°C)": result.get("input_summary", {}).get("temperature"),
        "Humidity (%)": result.get("input_summary", {}).get("humidity"),
        "Soil pH": result.get("input_summary", {}).get("ph"),
        "Rainfall (mm)": result.get("input_summary", {}).get("rainfall")
    }
    st.session_state.prediction_history.insert(0, record)
    st.session_state.last_prediction = result


def get_history_df() -> pd.DataFrame:
    """
    Retrieve prediction history as a pandas DataFrame.
    """
    if not st.session_state.get("prediction_history"):
        return pd.DataFrame()
    return pd.DataFrame(st.session_state.prediction_history)


def render_hero(title: str, subtitle: str, badge: str = "SMART CROP AI") -> None:
    """
    Render clean hero banner.
    """
    html = f"""
    <div class="hero-banner">
        <span class="crop-badge">{badge}</span>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(title: str, value: Any, desc: str = "", icon: str = "📊") -> None:
    """
    Render a modern agricultural KPI box.
    """
    html = f"""
    <div class="kpi-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="kpi-title">{title}</div>
            <div style="font-size: 1.2rem;">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-desc">{desc}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_info() -> None:
    """
    Render persistent sidebar metadata, badges, and quick links.
    """
    logo_path = os.path.join(PROJECT_ROOT, "assets", "logo.png")
    with st.sidebar:
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.markdown("<div style='font-size: 3rem; margin-bottom: 0.2rem;'>🌱</div>", unsafe_allow_html=True)
            
        st.markdown(
            """
            <div style="padding: 0.2rem 0.5rem 0.8rem 0.5rem;">
                <h2 style="color: #a7f3d0 !important; margin: 0; font-size: 1.4rem;">Smart Crop AI</h2>
                <p style="color: #6ee7b7; font-size: 0.82rem; margin-top: 0.2rem;">
                    Practical Crop Guidance for Your Farm
                </p>
            </div>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 0.4rem 0 1rem 0;">
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### 🌾 Farm Advisory")
        st.markdown(
            """
            - Enter your soil and weather conditions
            - Receive a suitable crop recommendation
            - Review seasonal growing guidance
            """
        )
        
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.75rem; color: #a7f3d0; opacity: 0.85;">
                Smart Crop Recommendation<br>
                Crop planning support for farmers
            </div>
            """,
            unsafe_allow_html=True
        )


def render_footer() -> None:
    """
    Render standard project footer.
    """
    st.markdown(
        """
        <div class="app-footer">
            <div style="margin-bottom: 0.5rem; font-weight: 600; color: #064e3b;">
                🌱 Smart Crop Recommendation
            </div>
            <div style="color: #64748b; font-size: 0.8rem;">
                Enter farm conditions, receive a crop suggestion, and review practical growing guidance.<br>
                Use alongside advice from local agricultural experts.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
