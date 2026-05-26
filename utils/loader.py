import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "glints_v2_cleaned.csv"
GDRIVE_URL = "https://drive.google.com/uc?id=1qIOvPXqbz-qkSwfMo2I_DAkJEq4pYccj"
@st.cache_data(show_spinner="Memuat dataset Glints...")
def load_data() -> pd.DataFrame:
    """
    Load cleaned CSV hasil export dari notebook.
    Di-cache oleh Streamlit agar tidak dibaca ulang setiap halaman.
    """
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH, low_memory=False)
    else:
        df = pd.read_csv(GDRIVE_URL, low_memory=False)

    # ── Pastikan tipe data kolom numerik benar ──
    numeric_cols = [
        'salary_min_monthly', 'salary_max_monthly',
        'salary_avg', 'salary_avg_usd', 'salary_avg_jt',
        'salary_min_usd', 'salary_max_usd',
        'salary_range_width_usd', 'salary_range_width_jt',
        'skill_count', 'education_rank',
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # ── Pastikan boolean has_salary benar ──
    if 'has_salary' in df.columns:
        df['has_salary'] = df['has_salary'].astype(bool)

    # ── Isi nilai kosong kolom kategorikal ──
    cat_cols = [
        'Industry', 'Job_Category_parent', 'Job_Category',
        'Job_Type_Label', 'Work_Arr_Label', 'Education_Label',
        'experience_level', 'salary_tier',
    ]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Tidak Diketahui')

    # ── Fallback: hitung salary_avg_usd jika belum ada di CSV ──
    if 'salary_avg_usd' not in df.columns and 'salary_avg' in df.columns:
        df['salary_avg_usd'] = df['salary_avg']

    return df


def get_salary_df(df: pd.DataFrame) -> pd.DataFrame:
    """Subset hanya baris yang punya data salary valid."""
    return df[df['has_salary'] == True].copy()
