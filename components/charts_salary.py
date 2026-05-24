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


def chart_salary_distribution(df_sal: pd.DataFrame) -> go.Figure:
    df_viz = df_sal[df_sal['salary_avg_jt'] <= 40].copy()
    median_val = df_viz['salary_avg_jt'].median()
    mean_val   = df_viz['salary_avg_jt'].mean()

    fig = px.histogram(
        df_viz, x='salary_avg_jt',
        nbins=60,
        title='Distribusi Avg Salary Bulanan (≤ 40 Jt)',
        color_discrete_sequence=[BLUE],
        opacity=0.85,
        labels={'salary_avg_jt': 'Gaji Rata-rata (Juta Rp/bulan)'},
    )
    fig.add_vline(x=median_val, line_dash='dash', line_color='red',
                  annotation_text=f'Median: {median_val:.1f} Jt',
                  annotation_position='top right')
    fig.add_vline(x=mean_val, line_dash='dash', line_color='orange',
                  annotation_text=f'Mean: {mean_val:.1f} Jt',
                  annotation_position='top left')
    fig.update_layout(**LAYOUT, height=360)
    fig.update_yaxes(showgrid=False, title='Frekuensi')
    return fig


def chart_salary_tier(df_sal: pd.DataFrame) -> go.Figure:
    tier = df_sal['salary_tier'].value_counts().reset_index()
    tier.columns = ['Tier', 'Jumlah']
    total = tier['Jumlah'].sum()
    tier['Pct'] = (tier['Jumlah'] / total * 100).round(1)

    fig = px.bar(
        tier, x='Tier', y='Jumlah',
        title='Distribusi Salary Tier',
        color='Tier',
        color_discrete_sequence=px.colors.sequential.YlOrRd,
        text=tier.apply(lambda r: f"{r['Jumlah']:,}\n({r['Pct']}%)", axis=1),
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(**LAYOUT, height=360, showlegend=False)
    fig.update_yaxes(showgrid=False, title='Jumlah Lowongan')
    fig.update_xaxes(title='')
    return fig


def chart_salary_by_industry(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    sal_ind = (
        df_sal.groupby('Industry')['salary_avg_jt']
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
        hovertemplate='Mean: %{x:.1f} Jt<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=sal_ind['Industry'], x=sal_ind['median'],
        orientation='h', name='Median',
        marker_color='#004AAD',
        width=0.4,
        hovertemplate='Median: %{x:.1f} Jt<extra></extra>',
        text=sal_ind['median'].round(1),
        texttemplate='%{text} Jt',
        textposition='outside',
    ))
    fig.update_layout(
        **LAYOUT,
        title=f'Top {n} Industri by Salary (Mean vs Median)',
        barmode='overlay',
        height=420,
        legend=dict(orientation='h', y=-0.15),
    )
    fig.update_xaxes(title='Gaji (Juta Rp/bulan)', showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(title='')
    return fig


def chart_salary_by_cluster(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    sal_cat = (
        df_sal.groupby('Job_Category_parent')['salary_avg_jt']
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
        hovertemplate='Mean: %{x:.1f} Jt<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=sal_cat['Job_Category_parent'], x=sal_cat['median'],
        orientation='h', name='Median',
        marker_color='#004AAD',
        width=0.4,
        text=sal_cat['median'].round(1),
        texttemplate='%{text} Jt',
        textposition='outside',
        hovertemplate='Median: %{x:.1f} Jt<extra></extra>',
    ))
    fig.update_layout(
        **LAYOUT,
        title=f'Top {n} Job Cluster by Salary (Mean vs Median)',
        barmode='overlay',
        height=420,
        legend=dict(orientation='h', y=-0.15),
    )
    fig.update_xaxes(title='Gaji (Juta Rp/bulan)', showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(title='')
    return fig


def chart_salary_box_jobtype(df_sal: pd.DataFrame) -> go.Figure:
    if 'Job_Type_Label' not in df_sal.columns:
        return go.Figure()
    df_viz = df_sal[df_sal['salary_avg_jt'] <= 30]
    order = (
        df_viz.groupby('Job_Type_Label')['salary_avg_jt']
        .median().sort_values(ascending=False).index.tolist()
    )
    fig = px.box(
        df_viz,
        x='Job_Type_Label', y='salary_avg_jt',
        category_orders={'Job_Type_Label': order},
        title='Distribusi Salary per Tipe Pekerjaan',
        color='Job_Type_Label',
        color_discrete_sequence=px.colors.qualitative.Set2,
        points=False,
        labels={'salary_avg_jt': 'Avg Salary (Juta Rp/bulan)', 'Job_Type_Label': ''},
    )
    fig.update_layout(**LAYOUT, height=380, showlegend=False)
    fig.update_yaxes(showgrid=True, gridcolor='#F0F2F6')
    return fig


def chart_bubble_demand_salary(df_sal: pd.DataFrame) -> go.Figure:
    bubble = (
        df_sal.groupby('Job_Category_parent').agg(
            count=('salary_avg_jt', 'count'),
            median_sal=('salary_avg_jt', 'median'),
            range_w=('salary_range_width_jt', 'median'),
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
        hover_data={'count': True, 'median_sal': ':.1f', 'range_w': ':.1f'},
        title='Bubble Chart: Demand vs Salary per Job Cluster',
        labels={
            'count': 'Jumlah Lowongan (Demand)',
            'median_sal': 'Median Salary (Juta Rp/bulan)',
        },
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_traces(textposition='top center', marker=dict(opacity=0.8, line_width=1.5))
    fig.add_hline(y=med_y, line_dash='dash', line_color='gray', opacity=0.5)
    fig.add_vline(x=med_x, line_dash='dash', line_color='gray', opacity=0.5)

    # Kuadran label
    x_max = bubble['count'].max()
    y_max = bubble['median_sal'].max()
    y_min = bubble['median_sal'].min()
    for txt, x, y, color in [
        ('High Demand\nHigh Salary', med_x * 1.05, y_max * 0.97, '#2E86AB'),
        ('Low Demand\nHigh Salary', med_x * 0.05, y_max * 0.97, '#55A868'),
        ('High Demand\nLow Salary', med_x * 1.05, y_min * 1.03, '#E07B54'),
        ('Low Demand\nLow Salary', med_x * 0.05, y_min * 1.03, '#9B9B9B'),
    ]:
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
                           font=dict(size=10, color=color), xanchor='left')

    fig.update_layout(**LAYOUT, height=520, showlegend=False)
    fig.update_xaxes(showgrid=True, gridcolor='#F0F2F6')
    fig.update_yaxes(showgrid=True, gridcolor='#F0F2F6')
    return fig


def chart_heatmap_industry_exp(df_sal: pd.DataFrame) -> None:
    """Render seaborn heatmap via st.pyplot (annotated values)."""
    import streamlit as st

    top12 = df_sal['Industry'].value_counts().head(12).index
    levels = [l for l in LEVEL_ORDER if l in df_sal['experience_level'].unique()]

    hm = (
        df_sal[df_sal['Industry'].isin(top12)]
        .pivot_table(index='Industry', columns='experience_level',
                     values='salary_avg_jt', aggfunc='median')
        .reindex(columns=levels)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    sns.heatmap(
        hm, annot=True, fmt='.1f',
        cmap='YlOrRd', linewidths=0.5, ax=ax,
        cbar_kws={'label': 'Median Salary (Jt Rp)', 'shrink': 0.8},
    )
    ax.set_title('Heatmap Median Salary — Top 12 Industri × Experience Level',
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
    sal_edu = (
        df_sal.groupby('Education_Label')['salary_avg_jt']
        .agg(median='median', mean='mean', count='count')
        .reset_index()
        .sort_values('median', ascending=True)
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sal_edu['Education_Label'], x=sal_edu['mean'],
        orientation='h', name='Mean',
        marker_color='#A0C4FF', opacity=0.6,
    ))
    fig.add_trace(go.Bar(
        y=sal_edu['Education_Label'], x=sal_edu['median'],
        orientation='h', name='Median',
        marker_color='#004AAD', width=0.4,
        text=sal_edu['median'].round(1),
        texttemplate='%{text} Jt', textposition='outside',
    ))
    fig.update_layout(
        **LAYOUT,
        title='Salary per Tingkat Pendidikan',
        barmode='overlay', height=360,
        legend=dict(orientation='h', y=-0.2),
    )
    fig.update_xaxes(title='Gaji (Juta Rp/bulan)')
    fig.update_yaxes(title='')
    return fig


def chart_top_salary_category(df_sal: pd.DataFrame, n: int = 10) -> go.Figure:
    top = (
        df_sal.groupby('Job_Category')['salary_avg_jt']
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
        text=top.apply(lambda r: f"{r['median']:.1f} Jt\n(n={int(r['count'])})", axis=1),
        labels={'median': 'Median Salary (Jt)', 'Job_Category': ''},
    )
    fig.update_traces(textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=400, showlegend=False)
    fig.update_xaxes(tickangle=-30)
    fig.update_yaxes(showgrid=False, title='Median Salary (Juta Rp/bulan)')
    return fig
