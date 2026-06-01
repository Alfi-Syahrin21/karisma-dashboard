import streamlit as st
from pathlib import Path

# ── Konfigurasi halaman ──
st.set_page_config(
    page_title="Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Halaman landing ──
st.markdown("""
<div class="page-header">
    <h1>📊 Job Market Dashboard</h1>
    <p>Analisis mendalam pasar kerja Indonesia — berdasarkan platform Glints</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Selamat datang! Gunakan **navigasi di sidebar kiri** untuk menjelajahi dashboard.

| Halaman | Isi |
|---|---|
| 🏠 Overview | KPI utama, ringkasan dataset, dan 7 insight tajam |
| 📊 Job Market | Distribusi industri, job cluster, tipe & arrangement pekerjaan |
| 💰 Salary Analysis | Distribusi salary, perbandingan per industri, experience, pendidikan |
| 🛠 Skill Analysis | Top skills, skill premium, dan skill paling versatile |
| 🔍 Job Explorer | Filter & cari lowongan spesifik secara interaktif |
""")

st.info("Gunakan **Filter Global** di sidebar untuk memfilter data di semua halaman sekaligus.", icon="💡")
