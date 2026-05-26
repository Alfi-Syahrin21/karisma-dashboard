import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils.loader import load_data, get_salary_df
from utils.filters import render_sidebar_filters

st.set_page_config(page_title="Job Explorer — Dashboard", page_icon="🔍", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Data ──
df_raw = load_data()
df     = render_sidebar_filters(df_raw)
df_sal = get_salary_df(df)

# ── Helper kolom USD ──
SAL_COL = 'salary_avg_usd' if 'salary_avg_usd' in df.columns else 'salary_avg'

# ── Header ──
st.markdown("""
<div class="page-header">
    <h1>🔍 Job Explorer</h1>
    <p>Cari dan filter lowongan spesifik, serta lihat posisi tiap job category di kuadran Demand × Salary</p>
</div>
""", unsafe_allow_html=True)

# ── Filter tambahan spesifik halaman ini ──
st.markdown('<p class="section-label">Filter Tambahan</p>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    keyword = st.text_input("🔎 Cari judul pekerjaan", placeholder="contoh: Data Analyst, Frontend...")

with col_f2:
    if SAL_COL in df.columns:
        sal_max = int(df[SAL_COL].quantile(0.99)) if df[SAL_COL].notna().any() else 5000
        salary_range = st.slider(
            "Rentang Salary (USD/month)",
            min_value=0, max_value=max(sal_max, 2000), value=(0, min(sal_max, 2000)), step=50,
        )
    else:
        salary_range = (0, 2000)

with col_f3:
    has_salary_only = st.checkbox("Hanya tampilkan yang ada data salary", value=False)

# ── Terapkan filter tambahan ──
df_exp = df.copy()

if keyword:
    df_exp = df_exp[df_exp['Title'].str.contains(keyword, case=False, na=False)]

if has_salary_only:
    df_exp = df_exp[df_exp['has_salary'] == True]

if SAL_COL in df_exp.columns:
    df_exp = df_exp[
        (df_exp[SAL_COL].isna()) |
        (df_exp[SAL_COL].between(salary_range[0], salary_range[1]))
    ]

st.caption(f"Ditemukan **{len(df_exp):,}** lowongan.")

st.markdown("---")

# ── Tabel Lowongan ──
st.markdown('<p class="section-label">Daftar Lowongan</p>', unsafe_allow_html=True)

display_cols = [c for c in [
    'Title', 'Industry', 'Job_Category_parent', 'Job_Category',
    'Job_Type_Label', 'Work_Arr_Label', 'experience_level',
    SAL_COL, 'salary_tier', 'Education_Label', 'Job_Link',
] if c in df_exp.columns]

df_display = df_exp[display_cols].copy()
if SAL_COL in df_display.columns:
    df_display[SAL_COL] = df_display[SAL_COL].round(0)

rename_map = {
    'Title': 'Judul', 'Industry': 'Industri',
    'Job_Category_parent': 'Job Cluster', 'Job_Category': 'Job Category',
    'Job_Type_Label': 'Tipe', 'Work_Arr_Label': 'Arrangement',
    'experience_level': 'Experience',
    SAL_COL: 'Salary (USD/mo)',
    'salary_tier': 'Tier', 'Education_Label': 'Pendidikan', 'Job_Link': 'Link',
}
df_display = df_display.rename(columns=rename_map)

st.dataframe(
    df_display.head(500),
    use_container_width=True,
    height=380,
    column_config={
        "Link": st.column_config.LinkColumn("Link", display_text="Buka ↗"),
        "Salary (USD/mo)": st.column_config.NumberColumn("Salary (USD/mo)", format="$%.0f"),
    },
)

if len(df_exp) > 500:
    st.caption("⚠️ Menampilkan 500 baris pertama. Gunakan filter untuk mempersempit hasil.")

st.markdown("---")

# ── Demand × Salary Quadrant ──
st.markdown('<p class="section-label">Demand × Salary Quadrant</p>', unsafe_allow_html=True)
st.markdown("#### Posisi tiap Job Category di matriks Demand × Median Salary")

df_sal_exp = get_salary_df(df_exp)

if len(df_sal_exp) > 10:
    sal_col_exp = 'salary_avg_usd' if 'salary_avg_usd' in df_sal_exp.columns else 'salary_avg'
    cat_matrix = (
        df_sal_exp.groupby('Job_Category')
        .agg(count=(sal_col_exp, 'count'), median_sal=(sal_col_exp, 'median'))
        .query('count >= 5')
        .reset_index()
    )
    med_c = cat_matrix['count'].median()
    med_s = cat_matrix['median_sal'].median()

    cat_matrix['Kuadran'] = cat_matrix.apply(lambda r: (
        'High Demand + High Salary' if r['count'] >= med_c and r['median_sal'] >= med_s
        else 'High Demand + Low Salary' if r['count'] >= med_c
        else 'Low Demand + High Salary' if r['median_sal'] >= med_s
        else 'Low Demand + Low Salary'
    ), axis=1)

    color_map = {
        'High Demand + High Salary': '#2196F3',
        'High Demand + Low Salary':  '#F44336',
        'Low Demand + High Salary':  '#4CAF50',
        'Low Demand + Low Salary':   '#9E9E9E',
    }

    fig_quad = px.scatter(
        cat_matrix,
        x='count', y='median_sal',
        color='Kuadran',
        color_discrete_map=color_map,
        text='Job_Category',
        title='Demand × Salary Matrix — Job Category Level 3',
        labels={
            'count': 'Jumlah Lowongan (Demand)',
            'median_sal': 'Median Salary (USD/month)',
            'Job_Category': 'Job Category',
        },
        hover_data={'count': True, 'median_sal': ':,.0f'},
        opacity=0.8,
        size='count',
        size_max=30,
    )
    fig_quad.update_traces(textposition='top center', marker_line_width=0.5)
    fig_quad.add_hline(y=med_s, line_dash='dash', line_color='gray', opacity=0.4)
    fig_quad.add_vline(x=med_c, line_dash='dash', line_color='gray', opacity=0.4)
    fig_quad.update_layout(
        font_family="DM Sans, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        height=520,
        legend=dict(orientation='h', y=-0.18),
    )
    fig_quad.update_xaxes(showgrid=True, gridcolor='#F0F2F6')
    fig_quad.update_yaxes(showgrid=True, gridcolor='#F0F2F6', title='Median Salary (USD/month)')
    st.plotly_chart(fig_quad, use_container_width=True)

    # Ringkasan per kuadran
    st.markdown("##### Ringkasan per Kuadran")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    for col, quad, color in zip(
        [col_q1, col_q2, col_q3, col_q4],
        ['High Demand + High Salary', 'High Demand + Low Salary',
         'Low Demand + High Salary', 'Low Demand + Low Salary'],
        ['#2196F3', '#F44336', '#4CAF50', '#9E9E9E'],
    ):
        sub = cat_matrix[cat_matrix['Kuadran'] == quad]
        with col:
            st.metric(label=quad, value=f"{len(sub)} kategori")
else:
    st.info("Data tidak cukup untuk membuat kuadran. Coba perluas filter.")
