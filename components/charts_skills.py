import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BLUE   = '#2E86AB'
ORANGE = '#E07B54'

LAYOUT = dict(
    font_family="DM Sans, sans-serif",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(bgcolor='white', font_size=12),
)


def _explode_skills(df: pd.DataFrame) -> pd.Series:
    """Pecah kolom Skills (comma-separated) jadi Series per skill."""
    return (
        df['Skills'].dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .loc[lambda s: s != '']
    )

def _sal_col(df: pd.DataFrame) -> str:
    return 'salary_avg_usd' if 'salary_avg_usd' in df.columns else 'salary_avg'


def chart_top_skills(df: pd.DataFrame, n: int = 25) -> go.Figure:
    skills = _explode_skills(df)
    top = skills.value_counts().head(n).reset_index()
    top.columns = ['Skill', 'Frekuensi']

    fig = px.bar(
        top.sort_values('Frekuensi'),
        x='Frekuensi', y='Skill',
        orientation='h',
        title=f'Top {n} Skills Paling Dibutuhkan',
        color='Frekuensi',
        color_continuous_scale='reds',
        text='Frekuensi',
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=660)
    fig.update_xaxes(showgrid=False, title='Frekuensi')
    fig.update_yaxes(title='')
    return fig


def chart_skill_premium(df_sal: pd.DataFrame, n: int = 20) -> go.Figure:
    """Bar chart skill vs median salary USD — highlight atas/bawah median pasar."""
    col = _sal_col(df_sal)
    rows = []
    for _, row in df_sal.iterrows():
        if pd.isna(row.get('Skills')):
            continue
        for sk in str(row['Skills']).split(','):
            sk = sk.strip()
            if sk:
                rows.append({'skill': sk, 'salary': row[col]})

    if not rows:
        return go.Figure()

    skill_df = pd.DataFrame(rows)
    agg = (
        skill_df.groupby('skill')['salary']
        .agg(median='median', count='count')
        .query('count >= 30')
        .sort_values('median', ascending=False)
        .head(n)
        .sort_values('median')
        .reset_index()
    )
    overall_median = df_sal[col].median()
    agg['warna'] = agg['median'].apply(
        lambda v: 'Di atas median pasar' if v >= overall_median else 'Di bawah median pasar'
    )
    color_map = {'Di atas median pasar': BLUE, 'Di bawah median pasar': ORANGE}

    fig = px.bar(
        agg,
        x='median', y='skill',
        orientation='h',
        color='warna',
        color_discrete_map=color_map,
        title=f'Top {n} Skill — Median Salary Tertinggi (min 30 lowongan)',
        text=agg['median'].round(0).astype(int),
        labels={'median': 'Median Salary (USD/month)', 'skill': ''},
    )
    fig.update_traces(texttemplate='$%{text:,}', textposition='outside')
    fig.add_vline(
        x=overall_median, line_dash='dash', line_color='gray',
        annotation_text=f'Median pasar: ${overall_median:,.0f}',
        annotation_position='top right',
    )
    fig.update_layout(
        **LAYOUT, height=560,
        legend=dict(title='', orientation='h', y=-0.12),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#F0F2F6', title='Median Salary (USD/month)')
    fig.update_yaxes(title='')
    return fig


def chart_skill_versatile(df: pd.DataFrame, n: int = 15) -> go.Figure:
    """Bar chart skill berdasarkan jumlah industri unik tempat ia muncul."""
    rows = []
    for _, row in df.iterrows():
        if pd.isna(row.get('Skills')):
            continue
        for sk in str(row['Skills']).split(','):
            sk = sk.strip()
            if sk:
                rows.append({'skill': sk, 'industry': row['Industry']})

    if not rows:
        return go.Figure()

    skill_ind = pd.DataFrame(rows)
    freq = skill_ind['skill'].value_counts().reset_index()
    freq.columns = ['skill', 'total_freq']

    versatility = (
        skill_ind.groupby('skill')['industry'].nunique()
        .reset_index(name='n_industries')
        .merge(freq, on='skill')
        .query('total_freq >= 50')
        .sort_values('n_industries', ascending=False)
        .head(n)
        .sort_values('n_industries')
    )

    fig = px.bar(
        versatility,
        x='n_industries', y='skill',
        orientation='h',
        title=f'Top {n} Skill Paling Versatile (Lintas Industri)',
        color='n_industries',
        color_continuous_scale='teal',
        text=versatility['n_industries'].apply(lambda v: f'{v} industri'),
        labels={'n_industries': 'Jumlah Industri Unik', 'skill': ''},
        hover_data={'total_freq': True},
    )
    fig.update_traces(textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=480)
    fig.update_xaxes(showgrid=False, title='Jumlah Industri Unik')
    fig.update_yaxes(title='')
    return fig


def chart_skill_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter: frekuensi vs jumlah industri per skill."""
    rows = []
    for _, row in df.iterrows():
        if pd.isna(row.get('Skills')):
            continue
        for sk in str(row['Skills']).split(','):
            sk = sk.strip()
            if sk:
                rows.append({'skill': sk, 'industry': row['Industry']})

    if not rows:
        return go.Figure()

    skill_ind = pd.DataFrame(rows)
    freq = skill_ind['skill'].value_counts().reset_index()
    freq.columns = ['skill', 'total_freq']
    versatility = (
        skill_ind.groupby('skill')['industry'].nunique()
        .reset_index(name='n_industries')
        .merge(freq, on='skill')
        .query('total_freq >= 30')
    )

    fig = px.scatter(
        versatility,
        x='total_freq', y='n_industries',
        text='skill',
        title='Frekuensi vs Jumlah Industri per Skill',
        labels={
            'total_freq': 'Frekuensi (Total Lowongan)',
            'n_industries': 'Jumlah Industri Unik',
        },
        color='n_industries',
        color_continuous_scale='Teal',
        size='total_freq',
        size_max=30,
        opacity=0.75,
    )
    fig.update_traces(textposition='top center', marker_line_width=0.5)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=480)
    fig.update_xaxes(showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(showgrid=True, gridcolor='#F0F2F6')
    return fig
