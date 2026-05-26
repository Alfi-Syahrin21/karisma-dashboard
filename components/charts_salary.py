import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

BLUE   = '#2E86AB'
ORANGE = '#E07B54'

LAYOUT = dict(
    font_family="DM Sans, sans-serif",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(bgcolor='white', font_size=12),
)

LEVEL_ORDER = [
    'Entry Level (0 thn)',
    'Junior (1-3 thn)',
    'Mid Level (3-5 thn)',
    'Senior (5-10 thn)',
    'Expert (10+ thn)',
]

# ── Helper: kolom USD yang tersedia ─────────────────────────────────────────
def _sal_col(df: pd.DataFrame) -> str:
    """Kembalikan nama kolom salary USD yang tersedia di dataframe."""
    return 'salary_avg_usd' if 'salary_avg_usd' in df.columns else 'salary_avg'

def _range_col(df: pd.DataFrame) -> str:
    return 'salary_range_width_usd' if 'salary_range_width_usd' in df.columns else 'salary_range_width_jt'


def chart_salary_distribution(df_sal: pd.DataFrame) -> go.Figure:
    col = _sal_col(df_sal)
    df_viz = df_sal[df_sal[col] <= 2000].copy()   # cap $2,000/bulan untuk viz
    median_val = df_viz[col].median()
    mean_val   = df_viz[col].mean()

    fig = px.histogram(
        df_viz, x=col,
        nbins=60,
        title='Distribusi Avg Salary Bulanan (≤ $2,000)',
        color_discrete_sequence=[BLUE],
        opacity=0.85,
        labels={col: 'Avg Salary (USD/month)'},
    )
    fig.add_vline(x=median_val, line_dash='dash', line_color='red',
                  annotation_text=f'Median: ${median_val:,.0f}',
                  annotation_position='top right')
    fig.add_vline(x=mean_val, line_dash='dash', line_color='orange',
                  annotation_text=f'Mean: ${mean_val:,.0f}',
                  annotation_position='top left')
    fig.update_layout(**LAYOUT, height=360)
    fig.update_xaxes(title='Avg Salary (USD/month)')
    fig.update_yaxes(showgrid=False, title='Frekuensi')
    return fig


def chart_salary_tier(df_sal: pd.DataFrame) -> go.Figure:
    tier = df_sal['salary_tier'].value_counts().reset_index()
    tier.columns = ['Tier', 'Jumlah']
    total = tier['Jumlah'].sum()
    tier['Pct'] = (tier['Jumlah'] / total * 100).round(1)

    fig = px.bar(
        tier, x='Tier', y='Jumlah',
        title='Distribusi Salary Tier (USD/month)',
        color='Tier',
        color_discrete_sequence=px.colors.sequential.YlOrRd,
        text=tier.apply(lambda r: f"{r['Jumlah']:,}\n({r['Pct']}%)", axis=1),
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(**LAYOUT, height=360, showlegend=False)
    fig.update_yaxes(showgrid=False, title='Jumlah Lowongan')
    fig.update_xaxes(title='Salary Tier (USD/month)')
    return fig


def chart_salary_by_industry(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    col = _sal_col(df_sal)
    sal_ind = (
        df_sal.groupby('Industry')[col]
        .agg(median='median', mean='mean', count='count')
        .query('count >= 30')
        .sort_values('median', ascending=False)
        .head(n)
        .sort_values('median', ascending=True)
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sal_ind['Industry'], x=sal_ind['mean'],
        orientation='h', name='Mean',
        marker_color='#A0C4FF', opacity=0.6,
        hovertemplate='Mean: $%{x:,.0f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=sal_ind['Industry'], x=sal_ind['median'],
        orientation='h', name='Median',
        marker_color='#004AAD',
        width=0.4,
        hovertemplate='Median: $%{x:,.0f}<extra></extra>',
        text=sal_ind['median'].round(0).astype(int),
        texttemplate='$%{text:,}',
        textposition='outside',
    ))
    fig.update_layout(
        **LAYOUT,
        title=f'Top {n} Industri by Salary (Mean vs Median)',
        barmode='overlay',
        height=420,
        legend=dict(orientation='h', y=-0.15),
    )
    fig.update_xaxes(title='Avg Salary (USD/month)', showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(title='')
    return fig


def chart_salary_by_cluster(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    col = _sal_col(df_sal)
    sal_cat = (
        df_sal.groupby('Job_Category_parent')[col]
        .agg(median='median', mean='mean', count='count')
        .query('count >= 20')
        .sort_values('median', ascending=False)
        .head(n)
        .sort_values('median', ascending=True)
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sal_cat['Job_Category_parent'], x=sal_cat['mean'],
        orientation='h', name='Mean',
        marker_color='#A0C4FF', opacity=0.6,
        hovertemplate='Mean: $%{x:,.0f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=sal_cat['Job_Category_parent'], x=sal_cat['median'],
        orientation='h', name='Median',
        marker_color='#004AAD',
        width=0.4,
        text=sal_cat['median'].round(0).astype(int),
        texttemplate='$%{text:,}',
        textposition='outside',
        hovertemplate='Median: $%{x:,.0f}<extra></extra>',
    ))
    fig.update_layout(
        **LAYOUT,
        title=f'Top {n} Job Cluster by Salary (Mean vs Median)',
        barmode='overlay',
        height=420,
        legend=dict(orientation='h', y=-0.15),
    )
    fig.update_xaxes(title='Avg Salary (USD/month)', showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(title='')
    return fig


def chart_salary_box_jobtype(df_sal: pd.DataFrame) -> go.Figure:
    if 'Job_Type_Label' not in df_sal.columns:
        return go.Figure()
    col = _sal_col(df_sal)
    df_viz = df_sal[df_sal[col] <= 2000]
    order = (
        df_viz.groupby('Job_Type_Label')[col]
        .median().sort_values(ascending=False).index.tolist()
    )
    fig = px.box(
        df_viz,
        x='Job_Type_Label', y=col,
        category_orders={'Job_Type_Label': order},
        title='Distribusi Salary per Tipe Pekerjaan',
        color='Job_Type_Label',
        color_discrete_sequence=px.colors.qualitative.Set2,
        points=False,
        labels={col: 'Avg Salary (USD/month)', 'Job_Type_Label': ''},
    )
    fig.update_layout(**LAYOUT, height=380, showlegend=False)
    fig.update_yaxes(showgrid=True, gridcolor='#F0F2F6', title='Avg Salary (USD/month)')
    return fig


def chart_bubble_demand_salary(df_sal: pd.DataFrame) -> go.Figure:
    col     = _sal_col(df_sal)
    rcol    = _range_col(df_sal)
    bubble = (
        df_sal.groupby('Job_Category_parent').agg(
            count=(col, 'count'),
            median_sal=(col, 'median'),
            range_w=(rcol, 'median'),
        ).reset_index()
    )
    bubble['range_w'] = bubble['range_w'].fillna(0)
    med_x = bubble['count'].median()
    med_y = bubble['median_sal'].median()

    fig = px.scatter(
        bubble,
        x='count', y='median_sal',
        size='range_w',
        size_max=55,
        color='Job_Category_parent',
        text='Job_Category_parent',
        hover_data={'count': True, 'median_sal': ':,.0f', 'range_w': ':,.0f'},
        title='Bubble Chart: Demand vs Salary per Job Cluster',
        labels={
            'count': 'Jumlah Lowongan (Demand)',
            'median_sal': 'Median Salary (USD/month)',
        },
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_traces(textposition='top center', marker=dict(opacity=0.8, line_width=1.5))
    fig.add_hline(y=med_y, line_dash='dash', line_color='gray', opacity=0.5)
    fig.add_vline(x=med_x, line_dash='dash', line_color='gray', opacity=0.5)

    x_max = bubble['count'].max()
    y_max = bubble['median_sal'].max()
    y_min = bubble['median_sal'].min()
    for txt, x, y, color in [
        ('High Demand\nHigh Salary', med_x * 1.05, y_max * 0.97, '#2E86AB'),
        ('Low Demand\nHigh Salary',  med_x * 0.05, y_max * 0.97, '#55A868'),
        ('High Demand\nLow Salary',  med_x * 1.05, y_min * 1.03, '#E07B54'),
        ('Low Demand\nLow Salary',   med_x * 0.05, y_min * 1.03, '#9B9B9B'),
    ]:
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
                           font=dict(size=10, color=color), xanchor='left')

    fig.update_layout(**LAYOUT, height=520, showlegend=False)
    fig.update_xaxes(showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(showgrid=True, gridcolor='#F0F2F6', title='Median Salary (USD/month)')
    return fig


def chart_heatmap_industry_exp(df_sal: pd.DataFrame) -> None:
    """Render seaborn heatmap via st.pyplot (annotated values)."""
    col = _sal_col(df_sal)

    top12  = df_sal['Industry'].value_counts().head(12).index
    levels = [l for l in LEVEL_ORDER if l in df_sal['experience_level'].unique()]

    hm = (
        df_sal[df_sal['Industry'].isin(top12)]
        .pivot_table(index='Industry', columns='experience_level',
                     values=col, aggfunc='median')
        .reindex(columns=levels)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    sns.heatmap(
        hm, annot=True, fmt='.0f',
        cmap='YlOrRd', linewidths=0.5, ax=ax,
        cbar_kws={'label': 'Median Salary (USD/month)', 'shrink': 0.8},
    )
    ax.set_title('Heatmap Median Salary — Top 12 Industri × Experience Level (USD/month)',
                 fontsize=13, fontweight='bold', pad=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right', fontsize=9)
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def chart_salary_by_education(df_sal: pd.DataFrame) -> go.Figure:
    if 'Education_Label' not in df_sal.columns:
        return go.Figure()
    col = _sal_col(df_sal)
    sal_edu = (
        df_sal.groupby('Education_Label')[col]
        .agg(median='median', mean='mean', count='count')
        .reset_index()
        .sort_values('median', ascending=True)
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sal_edu['Education_Label'], x=sal_edu['mean'],
        orientation='h', name='Mean',
        marker_color='#A0C4FF', opacity=0.6,
        hovertemplate='Mean: $%{x:,.0f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=sal_edu['Education_Label'], x=sal_edu['median'],
        orientation='h', name='Median',
        marker_color='#004AAD', width=0.4,
        text=sal_edu['median'].round(0).astype(int),
        texttemplate='$%{text:,}', textposition='outside',
        hovertemplate='Median: $%{x:,.0f}<extra></extra>',
    ))
    fig.update_layout(
        **LAYOUT,
        title='Salary per Tingkat Pendidikan (USD/month)',
        barmode='overlay', height=360,
        legend=dict(orientation='h', y=-0.2),
    )
    fig.update_xaxes(title='Avg Salary (USD/month)')
    fig.update_yaxes(title='')
    return fig


def chart_top_salary_category(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    col = _sal_col(df_sal)
    top = (
        df_sal.groupby('Job_Category')[col]
        .agg(median='median', count='count')
        .query('count >= 10')
        .sort_values('median', ascending=False)
        .head(n)
        .reset_index()
    )
    fig = px.bar(
        top,
        x='Job_Category', y='median',
        title=f'Top {n} Job Category — Median Salary Tertinggi',
        color='median',
        color_continuous_scale='Reds',
        text=top.apply(lambda r: f"${r['median']:,.0f}\n(n={int(r['count'])})", axis=1),
        labels={'median': 'Median Salary (USD/month)', 'Job_Category': ''},
    )
    fig.update_traces(textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=400, showlegend=False)
    fig.update_xaxes(tickangle=-30)
    fig.update_yaxes(showgrid=False, title='Median Salary (USD/month)')
    return fig
