import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BLUE   = '#2E86AB'
ORANGE = '#E07B54'
GREEN  = '#55A868'
COLORS = px.colors.qualitative.Set2

LAYOUT = dict(
    font_family="DM Sans, sans-serif",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(bgcolor='white', font_size=12),
)


def chart_top_industry(df: pd.DataFrame, n: int = 15) -> go.Figure:
    top = df['Industry'].value_counts().head(n).reset_index()
    top.columns = ['Industry', 'Jumlah']
    fig = px.bar(
        top.sort_values('Jumlah'),
        x='Jumlah', y='Industry',
        orientation='h',
        title=f'Top {n} Industri — Jumlah Lowongan',
        color='Jumlah',
        color_continuous_scale='Blues',
        text='Jumlah',
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=420)
    fig.update_xaxes(showgrid=False, title='')
    fig.update_yaxes(title='')
    return fig


def chart_top_cluster(df: pd.DataFrame, n: int = 15) -> go.Figure:
    top = df['Job_Category_parent'].value_counts().head(n).reset_index()
    top.columns = ['Job Cluster', 'Jumlah']
    fig = px.bar(
        top.sort_values('Jumlah'),
        x='Jumlah', y='Job Cluster',
        orientation='h',
        title=f'Top {n} Job Cluster (Domain)',
        color='Job Cluster',
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text='Jumlah',
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(**LAYOUT, height=420, showlegend=False)
    fig.update_xaxes(showgrid=False, title='')
    fig.update_yaxes(title='')
    return fig


def chart_top_job_category(df: pd.DataFrame, n: int = 20) -> go.Figure:
    top = df['Job_Category'].value_counts().head(n).reset_index()
    top.columns = ['Job Category', 'Jumlah']
    fig = px.bar(
        top.sort_values('Jumlah'),
        x='Jumlah', y='Job Category',
        orientation='h',
        title=f'Top {n} Job Category — Paling Banyak Lowongan',
        color='Jumlah',
        color_continuous_scale='Reds',
        text='Jumlah',
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**LAYOUT, height=540)
    fig.update_xaxes(showgrid=False, title='')
    fig.update_yaxes(title='')
    return fig


def chart_job_type_pie(df: pd.DataFrame) -> go.Figure:
    if 'Job_Type_Label' not in df.columns:
        return go.Figure()
    counts = df['Job_Type_Label'].value_counts()
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title='Distribusi Tipe Pekerjaan',
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.45,
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(**LAYOUT, height=340, showlegend=False)
    return fig


def chart_work_arr_pie(df: pd.DataFrame) -> go.Figure:
    if 'Work_Arr_Label' not in df.columns:
        return go.Figure()
    counts = df['Work_Arr_Label'].value_counts()
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title='Work Arrangement',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.45,
    )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(**LAYOUT, height=340, showlegend=False)
    return fig


def chart_exp_level_bar(df: pd.DataFrame) -> go.Figure:
    if 'experience_level' not in df.columns:
        return go.Figure()
    counts = df['experience_level'].value_counts().reset_index()
    counts.columns = ['Experience Level', 'Jumlah']
    fig = px.bar(
        counts,
        x='Experience Level', y='Jumlah',
        title='Distribusi Experience Level',
        color='Experience Level',
        color_discrete_sequence=px.colors.qualitative.Set3,
        text='Jumlah',
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(**LAYOUT, height=360, showlegend=False)
    fig.update_xaxes(title='')
    fig.update_yaxes(showgrid=False, title='')
    return fig


def chart_work_arr_by_cluster(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    if 'Work_Arr_Label' not in df.columns:
        return go.Figure()
    top_clusters = df['Job_Category_parent'].value_counts().head(top_n).index
    sub = df[df['Job_Category_parent'].isin(top_clusters)]
    pivot = (
        sub.groupby(['Job_Category_parent', 'Work_Arr_Label'])
        .size().reset_index(name='Jumlah')
    )
    fig = px.bar(
        pivot,
        x='Jumlah', y='Job_Category_parent',
        color='Work_Arr_Label',
        orientation='h',
        title=f'Work Arrangement per Job Cluster (Top {top_n})',
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='stack',
    )
    fig.update_layout(**LAYOUT, height=420)
    fig.update_xaxes(title='Jumlah Lowongan')
    fig.update_yaxes(title='')
    return fig
