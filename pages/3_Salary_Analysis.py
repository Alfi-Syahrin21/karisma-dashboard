import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils.loader import load_data, get_salary_df
from utils.filters import render_sidebar_filters
from components.charts_salary import (
    chart_salary_distribution, chart_salary_tier,
    chart_salary_by_industry, chart_salary_by_cluster,
    chart_salary_box_jobtype, chart_bubble_demand_salary,
    chart_heatmap_industry_exp, chart_salary_by_education,
    chart_top_salary_category,
)

st.set_page_config(page_title="Salary Analysis — Dashboard", page_icon="💰", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Data ──
df_raw = load_data()
df     = render_sidebar_filters(df_raw)
df_sal = get_salary_df(df)

# ── Header ──
st.markdown("""
<div class="page-header">
    <h1>💰 Salary Analysis</h1>
    <p>Distribusi dan perbandingan salary per industri, job cluster, tipe pekerjaan, dan pendidikan</p>
</div>
""", unsafe_allow_html=True)

if len(df_sal) == 0:
    st.warning("Tidak ada data salary untuk filter yang dipilih. Coba ubah filter di sidebar.")
    st.stop()

st.caption(f"Analisis berdasarkan **{len(df_sal):,}** lowongan yang memiliki data salary.")

# ── Section A: Distribusi ──
st.markdown('<p class="section-label">A — Distribusi Salary</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(chart_salary_distribution(df_sal), use_container_width=True)
with col2:
    st.plotly_chart(chart_salary_tier(df_sal), use_container_width=True)

st.markdown("---")

# ── Section B: Per Industri & Cluster ──
st.markdown('<p class="section-label">B — Salary per Industri & Job Cluster</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(chart_salary_by_industry(df_sal), use_container_width=True)
with col4:
    st.plotly_chart(chart_salary_by_cluster(df_sal), use_container_width=True)

st.markdown("---")

# ── Section C: Top Job Category & Box Plot ──
st.markdown('<p class="section-label">C — Top Job Category & Job Type</p>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(chart_top_salary_category(df_sal), use_container_width=True)
with col6:
    st.plotly_chart(chart_salary_box_jobtype(df_sal), use_container_width=True)

st.markdown("---")

# ── Section D: Bubble Chart ──
st.markdown('<p class="section-label">D — Demand vs Salary Matrix</p>', unsafe_allow_html=True)
st.plotly_chart(chart_bubble_demand_salary(df_sal), use_container_width=True)

st.markdown("---")

# ── Section E: Heatmap Industry × Experience ──
st.markdown('<p class="section-label">E — Heatmap Industri × Experience Level</p>', unsafe_allow_html=True)
chart_heatmap_industry_exp(df_sal)

st.markdown("---")

# ── Section F: Pendidikan ──
st.markdown('<p class="section-label">F — Salary per Tingkat Pendidikan</p>', unsafe_allow_html=True)
st.plotly_chart(chart_salary_by_education(df_sal), use_container_width=True)
