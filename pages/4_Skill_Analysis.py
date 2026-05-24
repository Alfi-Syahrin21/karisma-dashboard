import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils.loader import load_data, get_salary_df
from utils.filters import render_sidebar_filters
from components.charts_skills import (
    chart_top_skills, chart_skill_premium,
    chart_skill_versatile, chart_skill_scatter,
)

st.set_page_config(page_title="Skill Analysis — Dashboard", page_icon="🛠", layout="wide")

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
    <h1>🛠 Skill Analysis</h1>
    <p>Skill paling dibutuhkan, skill premium (korelasi dengan salary), dan skill paling versatile</p>
</div>
""", unsafe_allow_html=True)

# ── Section A: Top Skills ──
st.markdown('<p class="section-label">A — Top Skills Paling Dibutuhkan</p>', unsafe_allow_html=True)

n_skills = st.slider("Tampilkan top N skills", min_value=10, max_value=40, value=25, step=5)
st.plotly_chart(chart_top_skills(df, n=n_skills), use_container_width=True)

st.markdown("---")

# ── Section B: Skill Premium ──
st.markdown('<p class="section-label">B — Skill Premium (Korelasi Salary)</p>', unsafe_allow_html=True)

if len(df_sal) > 0:
    st.markdown(
        "Skill diurutkan berdasarkan **median salary** dari lowongan yang mensyaratkan skill tersebut. "
        "Hanya skill dengan minimal 30 lowongan yang ditampilkan.",
        help="Semakin tinggi median salary, semakin 'premium' skill tersebut di pasar."
    )
    st.plotly_chart(chart_skill_premium(df_sal), use_container_width=True)
else:
    st.info("Tidak ada data salary untuk filter yang dipilih.")

st.markdown("---")

# ── Section C: Skill Versatile ──
st.markdown('<p class="section-label">C — Skill Paling Versatile (Lintas Industri)</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(chart_skill_versatile(df), use_container_width=True)
with col2:
    st.markdown("#### Frekuensi vs Jumlah Industri")
    st.caption("Skill di kanan atas = populer DAN lintas industri (paling versatile).")
    st.plotly_chart(chart_skill_scatter(df), use_container_width=True)
