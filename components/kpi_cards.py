import streamlit as st
import pandas as pd


def render_kpi_cards(df: pd.DataFrame, df_sal: pd.DataFrame) -> None:
    """Render 4 KPI cards di baris atas halaman Overview."""
    col1, col2, col3, col4 = st.columns(4)

    total_jobs = len(df)
    pct_salary = df['has_salary'].mean() * 100 if 'has_salary' in df.columns else 0

    # Gunakan salary_avg_usd (USD/bulan); fallback ke salary_avg jika kolom belum ada
    sal_col = 'salary_avg_usd' if 'salary_avg_usd' in df_sal.columns else 'salary_avg'
    median_sal = df_sal[sal_col].median() if len(df_sal) > 0 else 0

    pct_remote = (
        (df['Work_Arr_Label'].str.upper() == 'REMOTE').mean() * 100
        if 'Work_Arr_Label' in df.columns else 0
    )

    with col1:
        st.metric(
            label="Total Lowongan",
            value=f"{total_jobs:,}",
            help="Jumlah total lowongan setelah filter diterapkan",
        )
    with col2:
        st.metric(
            label="Median Salary",
            value=f"${median_sal:,.0f}/mo",
            help="Median salary bulanan dalam USD (hanya posting dengan data salary)",
        )
    with col3:
        st.metric(
            label="Ada Data Salary",
            value=f"{pct_salary:.1f}%",
            help="Persentase lowongan yang mencantumkan salary",
        )
    with col4:
        st.metric(
            label="Remote Tersedia",
            value=f"{pct_remote:.1f}%",
            help="Persentase lowongan yang menawarkan remote work",
        )
