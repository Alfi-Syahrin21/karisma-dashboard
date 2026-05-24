import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils.loader import load_data, get_salary_df
from utils.filters import render_sidebar_filters
from components.kpi_cards import render_kpi_cards

# ── Config ──
st.set_page_config(page_title="Overview — Dashboard", page_icon="🏠", layout="wide")

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
    <h1>🏠 Overview</h1>
    <p>Ringkasan kondisi pasar kerja Indonesia berdasarkan data Glints</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──
render_kpi_cards(df, df_sal)

st.markdown("---")

# ── Treemap Industry × Job Cluster ──
import plotly.express as px

st.markdown('<p class="section-label">Komposisi Pasar</p>', unsafe_allow_html=True)
st.markdown("#### Distribusi Lowongan: Industri → Job Cluster")

treemap_data = (
    df.groupby(['Industry', 'Job_Category_parent'])
    .size().reset_index(name='Jumlah')
    .query('Jumlah >= 5')
)

if len(treemap_data) > 0:
    fig_tree = px.treemap(
        treemap_data,
        path=['Industry', 'Job_Category_parent'],
        values='Jumlah',
        color='Jumlah',
        color_continuous_scale='Blues',
        hover_data={'Jumlah': True},
    )
    fig_tree.update_layout(
        font_family="DM Sans, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        height=460,
        coloraxis_showscale=False,
    )
    fig_tree.update_traces(
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value:,}<extra></extra>',
        textinfo='label+value',
    )
    st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("---")

# ── 7 Insight Cards ──
st.markdown('<p class="section-label">Key Insights</p>', unsafe_allow_html=True)
st.markdown("#### 7 Insight Tajam Pasar Kerja Glints")

top_ind = df['Industry'].value_counts().idxmax() if len(df) > 0 else '-'
top_ind_cnt = df['Industry'].value_counts().max() if len(df) > 0 else 0
remote_pct = (df['Work_Arr_Label'].str.upper() == 'REMOTE').mean() * 100 if 'Work_Arr_Label' in df.columns else 0
entry_pct  = (df['experience_level'] == 'Entry Level (0 thn)').mean() * 100 if 'experience_level' in df.columns else 0

insights = [
    ("INSIGHT 1 — Industri Terbesar ≠ Gaji Terbaik",
     f"{top_ind} paling banyak lowongan ({top_ind_cnt:,} posting) tapi bukan industri dengan gaji tertinggi. "
     "Volume tinggi = oversupply kandidat = bargaining power lebih rendah. "
     "Industri IT justru lebih sepi listing tapi gaji 2–3× lebih tinggi."),
    ("INSIGHT 2 — Remote Work Bukan Hak Semua Orang",
     f"Hanya {remote_pct:.1f}% lowongan menawarkan remote. Terkonsentrasi di Tech & Marketing — "
     "hampir tidak ada di Operations & F&B. Remote adalah privilege domain tertentu, bukan norma pasar."),
    ("INSIGHT 3 — Entry Level Mendominasi tapi Persaingan Brutal",
     f"{entry_pct:.0f}%+ lowongan tidak mensyaratkan pengalaman. Kompetisi sangat tinggi — "
     "diferensiasi melalui sertifikasi atau portofolio menjadi kritis untuk menonjol dari crowd."),
    ("INSIGHT 4 — Skill Premium = Kelangkaan, Bukan Popularitas",
     "Skill teknis tertentu membawa median salary jauh di atas rata-rata. "
     "Bukan skill paling sering muncul, tapi supply langka + demand tinggi = premium berlipat."),
    ("INSIGHT 5 — Jebakan Karir: High Demand, Low Salary",
     "Beberapa job category masuk kuadran High Demand + Low Salary. "
     "Ratusan lowongan = kompetitor banyak = gaji tertekan. Zona oversupply yang harus dihindari job seeker salary-driven."),
    ("INSIGHT 6 — ROI Pendidikan Tidak Linear",
     "Gap salary SMA/SMK vs S1 lebih kecil dari yang dibayangkan. "
     "Namun S2/S3 membawa lompatan signifikan di Finance & Tech. "
     "Sertifikasi profesional sering lebih cost-effective dari S1."),
    ("INSIGHT 7 — Versatile vs Spesialis: Dua Strategi Berbeda",
     "Skill lintas industri memberikan portabilitas karir. Skill teknis spesialis memberikan premium salary. "
     "Formula optimal: 1 hard skill spesialis + 2–3 versatile skill untuk combination value tertinggi."),
]

col_a, col_b = st.columns(2)
for i, (title, body) in enumerate(insights):
    col = col_a if i % 2 == 0 else col_b
    with col:
        st.markdown(f"""
        <div class="insight-card">
            <strong>{title}</strong>
            {body}
        </div>
        """, unsafe_allow_html=True)
