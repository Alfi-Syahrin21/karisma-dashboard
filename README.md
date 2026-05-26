# 📊 Glints Job Market Dashboard


> **Live Demo:** [👉 Klik di sini untuk melihat dashboard](https://karisma-dashboard.streamlit.app/)

---

Dashboard analisis pasar kerja Indonesia.

## Struktur Proyek

```
karisma-dashboard/
├── app.py                        # Entry point
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Job_Market.py
│   ├── 3_Salary_Analysis.py
│   ├── 4_Skill_Analysis.py
│   └── 5_Job_Explorer.py
├── data/
│   └── glints_v2_cleaned.csv     # ← letakkan file CSV di sini
├── utils/
│   ├── loader.py
│   └── filters.py
├── components/
│   ├── kpi_cards.py
│   ├── charts_market.py
│   ├── charts_salary.py
│   └── charts_skills.py
├── assets/
│   └── style.css
├── .streamlit/
│   └── config.toml
└── requirements.txt
```

## Setup & Cara Menjalankan

```bash
# 1. Clone / download folder ini
cd karisma-dashboard

# 2. Buat virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Letakkan file CSV hasil export notebook
#    ke dalam folder data/glints_v2_cleaned.csv

# 5. Jalankan dashboard
streamlit run app.py
```
<!-- 
## Dataset

File `glints_v2_cleaned.csv` adalah hasil export dari notebook analisis (`glints_analysis_fixed_usd.ipynb`). -->

## Halaman

| Halaman | Deskripsi |
|---|---|
| Overview | KPI cards, treemap industri, 7 insight utama |
| Job Market | Top industri, job cluster, tipe pekerjaan, work arrangement |
| Salary Analysis | Distribusi salary, perbandingan per industri/experience/pendidikan |
| Skill Analysis | Top skills, skill premium, skill versatile |
| Job Explorer | Tabel interaktif + kuadran Demand × Salary |
