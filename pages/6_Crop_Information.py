"""
Crop Information Knowledge Base Page — Smart Crop AI.
Detailed agronomic profiles, cultivation guides, climatic requirements,
and empirical dataset benchmarks for all 22 supported crops.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Setup path and config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.crop_information import (
    CROP_DATABASE,
    get_crop_profile,
    get_all_crop_names,
    compute_empirical_crop_ranges
)
from utils.helpers import init_page, render_hero, render_kpi_card, render_sidebar_info, render_footer

init_page("Crop Information Knowledge Base", "📚")
render_sidebar_info()

render_hero(
    title="Agronomic Crop Knowledge Base",
    subtitle="Verified agronomic profiles, soil requirements, cultivation guides, and empirical dataset benchmarks for all 22 supported crop varieties.",
    badge="AGRICULTURAL KNOWLEDGE BASE"
)

# Load empirical dataset ranges
data_path = os.path.join(PROJECT_ROOT, "data", "crop_recommendation.csv")
empirical_data = compute_empirical_crop_ranges(data_path)

# Top search and filter bar
col_search, col_cat = st.columns([2, 1])

all_crops = get_all_crop_names()

with col_cat:
    categories = ["All Categories", "Cereals & Grains", "Pulses & Legumes", "Fruits & Horticulture", "Cash Crops & Fibers", "Beverages"]
    selected_cat = st.selectbox("Filter by Category:", options=categories)

# Map category filters
def matches_category(crop_key: str, cat_filter: str) -> bool:
    if cat_filter == "All Categories":
        return True
    profile = CROP_DATABASE.get(crop_key, {})
    c_type = profile.get("category", "").lower()
    if cat_filter == "Cereals & Grains":
        return "cereal" in c_type or "grain" in c_type
    elif cat_filter == "Pulses & Legumes":
        return "pulse" in c_type or "legume" in c_type
    elif cat_filter == "Fruits & Horticulture":
        return "fruit" in c_type or "horticulture" in c_type
    elif cat_filter == "Cash Crops & Fibers":
        return "fiber" in c_type or "cash" in c_type
    elif cat_filter == "Beverages":
        return "beverage" in c_type or "plantation" in c_type
    return True

filtered_crops = [c for c in all_crops if matches_category(c, selected_cat)]

with col_search:
    selected_crop_key = st.selectbox(
        "Select Crop to Inspect:",
        options=filtered_crops,
        format_func=lambda k: f"{CROP_DATABASE[k]['icon']} {CROP_DATABASE[k]['common_name']}"
    )

crop_info = get_crop_profile(selected_crop_key)

if crop_info:
    # Crop Header Card
    st.markdown(
        f"""
        <div class="agri-card agri-card-highlight" style="background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%); margin-top: 1rem;">
            <div style="display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap;">
                <div style="font-size: 4rem;">{crop_info['icon']}</div>
                <div>
                    <span class="crop-badge">{crop_info['category']}</span>
                    <h2 style="color: #064e3b; margin: 0.3rem 0; font-size: 2.2rem;">{crop_info['common_name']}</h2>
                    <div style="color: #059669; font-style: italic; font-size: 1.1rem; font-weight: 500;">
                        {crop_info['scientific_name']} &nbsp;|&nbsp; Family: {crop_info['family']}
                    </div>
                </div>
            </div>
            <p style="color: #334155; font-size: 1rem; line-height: 1.6; margin-top: 1rem;">
                {crop_info['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4 Key Agronomic Conditions
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Ideal Temperature", crop_info["ideal_temp_range"], "Optimal thermal window", "🌡️")
    with k2:
        render_kpi_card("Ideal Humidity", crop_info["ideal_humidity_range"], "Relative atmospheric humidity", "💧")
    with k3:
        render_kpi_card("Suitable Soil pH", crop_info["suitable_ph_range"], "Acidity / alkalinity tolerance", "🧪")
    with k4:
        render_kpi_card("Approx Rainfall", crop_info["rainfall_requirement"], "Hydrological requirement", "🌧️")

    st.markdown("<br>", unsafe_allow_html=True)

    # Comparison Table: General Agronomy vs. Dataset-Derived Empirical Data
    st.markdown("### ⚖️ General Agronomic Standards vs. Dataset-Derived Empirical Ranges")
    st.caption("Explicitly distinguishing published agronomic literature from the training dataset's statistical observations.")

    crop_emp = empirical_data.get(selected_crop_key, {})

    comp_rows = [
        {
            "Parameter": "Nitrogen (N)",
            "General Agronomic Guidance": "Requires balanced N supply during vegetative and tillering phases",
            "Dataset Min": f"{crop_emp.get('N', {}).get('min', 'N/A')} kg/ha",
            "Dataset Mean": f"{crop_emp.get('N', {}).get('mean', 'N/A')} kg/ha",
            "Dataset Max": f"{crop_emp.get('N', {}).get('max', 'N/A')} kg/ha"
        },
        {
            "Parameter": "Phosphorus (P)",
            "General Agronomic Guidance": "Critical for root proliferation, flowering, and energy transfer (ATP)",
            "Dataset Min": f"{crop_emp.get('P', {}).get('min', 'N/A')} kg/ha",
            "Dataset Mean": f"{crop_emp.get('P', {}).get('mean', 'N/A')} kg/ha",
            "Dataset Max": f"{crop_emp.get('P', {}).get('max', 'N/A')} kg/ha"
        },
        {
            "Parameter": "Potassium (K)",
            "General Agronomic Guidance": "Regulates stomatal opening, drought resilience, and fruit sugar concentration",
            "Dataset Min": f"{crop_emp.get('K', {}).get('min', 'N/A')} kg/ha",
            "Dataset Mean": f"{crop_emp.get('K', {}).get('mean', 'N/A')} kg/ha",
            "Dataset Max": f"{crop_emp.get('K', {}).get('max', 'N/A')} kg/ha"
        },
        {
            "Parameter": "Temperature",
            "General Agronomic Guidance": crop_info["ideal_temp_range"],
            "Dataset Min": f"{crop_emp.get('temperature', {}).get('min', 'N/A')} °C",
            "Dataset Mean": f"{crop_emp.get('temperature', {}).get('mean', 'N/A')} °C",
            "Dataset Max": f"{crop_emp.get('temperature', {}).get('max', 'N/A')} °C"
        },
        {
            "Parameter": "Humidity",
            "General Agronomic Guidance": crop_info["ideal_humidity_range"],
            "Dataset Min": f"{crop_emp.get('humidity', {}).get('min', 'N/A')} %",
            "Dataset Mean": f"{crop_emp.get('humidity', {}).get('mean', 'N/A')} %",
            "Dataset Max": f"{crop_emp.get('humidity', {}).get('max', 'N/A')} %"
        },
        {
            "Parameter": "Soil pH",
            "General Agronomic Guidance": crop_info["suitable_ph_range"],
            "Dataset Min": f"{crop_emp.get('ph', {}).get('min', 'N/A')}",
            "Dataset Mean": f"{crop_emp.get('ph', {}).get('mean', 'N/A')}",
            "Dataset Max": f"{crop_emp.get('ph', {}).get('max', 'N/A')}"
        },
        {
            "Parameter": "Rainfall",
            "General Agronomic Guidance": crop_info["rainfall_requirement"],
            "Dataset Min": f"{crop_emp.get('rainfall', {}).get('min', 'N/A')} mm",
            "Dataset Mean": f"{crop_emp.get('rainfall', {}).get('mean', 'N/A')} mm",
            "Dataset Max": f"{crop_emp.get('rainfall', {}).get('max', 'N/A')} mm"
        }
    ]

    df_comp_table = pd.DataFrame(comp_rows)
    st.dataframe(df_comp_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cultivation & Soil Details
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown(
            f"""
            <div class="agri-card">
                <h4 style="color: #064e3b; margin-top: 0;">🌱 Soil Suitability & Cropping Cycle</h4>
                <p><strong>Recommended Sowing Season:</strong> {crop_info.get('season', 'General')}</p>
                <p><strong>Approximate Crop Duration:</strong> {crop_info.get('growth_duration', 'Varies')}</p>
                <p><strong>Optimal Soil Types:</strong></p>
                <ul>
                    {''.join([f'<li>{s}</li>' for s in crop_info.get('soil_types', [])])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with g_col2:
        practices = crop_info.get("cultivation_practices", [])
        st.markdown(
            f"""
            <div class="agri-card">
                <h4 style="color: #064e3b; margin-top: 0;">🚜 Recommended Agronomic Practices</h4>
                <ul>
                    {''.join([f'<li style="margin-bottom: 0.5rem; line-height: 1.5;">{p}</li>' for p in practices])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# Master Table for all 22 Crops
with st.expander("📋 Browse Complete 22-Crop Master Agronomic Matrix"):
    matrix_rows = []
    for c_key in all_crops:
        p = CROP_DATABASE[c_key]
        matrix_rows.append({
            "Crop": f"{p['icon']} {p['common_name']}",
            "Category": p["category"].split("/")[0].strip(),
            "Season": p["season"],
            "Temp Range": p["ideal_temp_range"],
            "Humidity": p["ideal_humidity_range"],
            "Soil pH": p["suitable_ph_range"],
            "Rainfall": p["rainfall_requirement"],
            "Duration": p["growth_duration"]
        })
    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)

render_footer()
