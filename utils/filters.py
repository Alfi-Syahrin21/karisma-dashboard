import streamlit as st
import pandas as pd


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render filter global di sidebar dan return df yang sudah difilter.
    Dipanggil dari setiap halaman pages/.
    """
    with st.sidebar:
        st.markdown("## 🔎 Filter Data")
        st.markdown("---")

        # ── Industry ──
        industries = sorted(df['Industry'].dropna().unique().tolist())
        selected_industry = st.multiselect(
            "Industri",
            options=industries,
            default=[],
            placeholder="Semua industri",
        )

        # ── Job Type ──
        if 'Job_Type_Label' in df.columns:
            job_types = sorted(df['Job_Type_Label'].dropna().unique().tolist())
            selected_job_type = st.multiselect(
                "Tipe Pekerjaan",
                options=job_types,
                default=[],
                placeholder="Semua tipe",
            )
        else:
            selected_job_type = []

        # ── Work Arrangement ──
        if 'Work_Arr_Label' in df.columns:
            arrangements = sorted(df['Work_Arr_Label'].dropna().unique().tolist())
            selected_arr = st.multiselect(
                "Work Arrangement",
                options=arrangements,
                default=[],
                placeholder="Semua arrangement",
            )
        else:
            selected_arr = []

        # ── Experience Level ──
        if 'experience_level' in df.columns:
            exp_levels = sorted(df['experience_level'].dropna().unique().tolist())
            selected_exp = st.multiselect(
                "Experience Level",
                options=exp_levels,
                default=[],
                placeholder="Semua level",
            )
        else:
            selected_exp = []

        st.markdown("---")
        st.caption(f"Total data: **{len(df):,}** lowongan")

    # ── Terapkan filter ──
    filtered = df.copy()

    if selected_industry:
        filtered = filtered[filtered['Industry'].isin(selected_industry)]
    if selected_job_type:
        filtered = filtered[filtered['Job_Type_Label'].isin(selected_job_type)]
    if selected_arr:
        filtered = filtered[filtered['Work_Arr_Label'].isin(selected_arr)]
    if selected_exp:
        filtered = filtered[filtered['experience_level'].isin(selected_exp)]

    return filtered
