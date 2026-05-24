import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils.loader import load_data
from utils.filters import render_sidebar_filters
from components.charts_market import (
    chart_top_industry, chart_top_cluster, chart_top_job_category,
    chart_job_type_pie, chart_work_arr_pie, chart_exp_level_bar,
    chart_work_arr_by_cluster,
)

st.set_page_config(page_title="Job Market — Dashboard", page_icon="📊", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Data ──
df_raw = load_data()
df     = render_sidebar_filters(df_raw)

# ── Header ──
st.markdown("""
<div class="page-header">
    <h1>📊 Job Market Analysis</h1>
    <p>Distribusi lowongan berdasarkan industri, job cluster, tipe pekerjaan, dan experience</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Menampilkan **{len(df):,}** lowongan setelah filter diterapkan.")

# ── Section A: Industry & Cluster ──
st.markdown('<p class="section-label">A — Industri & Job Cluster</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(chart_top_industry(df), use_container_width=True)
with col2:
    st.plotly_chart(chart_top_cluster(df), use_container_width=True)

st.markdown("---")

# ── Section B: Top Job Category ──
st.markdown('<p class="section-label">B — Job Category (Level 3)</p>', unsafe_allow_html=True)

n_cat = st.slider("Tampilkan top N job category", min_value=10, max_value=30, value=20, step=5)
st.plotly_chart(chart_top_job_category(df, n=n_cat), use_container_width=True)

st.markdown("---")

# ── Section C: Distribusi Tipe & Arrangement ──
st.markdown('<p class="section-label">C — Tipe & Work Arrangement</p>', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    st.plotly_chart(chart_job_type_pie(df), use_container_width=True)
with col4:
    st.plotly_chart(chart_work_arr_pie(df), use_container_width=True)
with col5:
    st.plotly_chart(chart_exp_level_bar(df), use_container_width=True)

st.markdown("---")

# ── Section D: Work Arrangement per Cluster ──
st.markdown('<p class="section-label">D — Work Arrangement per Job Cluster</p>', unsafe_allow_html=True)
st.plotly_chart(chart_work_arr_by_cluster(df), use_container_width=True)
