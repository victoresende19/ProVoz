import pandas as pd
import numpy as np
import plotly.express as px

def pie_plot(df: pd.DataFrame, coluna: str, titulo = str):
    """
    Recebe um dataframe para fazer a plotagem dos dados.
    
    Parâmetros:
    - df: dataframe com as informações
    - coluna: nome da coluna
    - titulo: titulo desejado

    Retorna:
    - Gráfico de pizza
    """

    data = df[coluna].value_counts().reset_index()
    data.columns = [coluna, 'count']  

    fig = px.pie(data, names=coluna, values='count', color_discrete_sequence=['#778da9','#555b6e', '#577590', '#8e9aaf', '#d3d3d3'],
                hole=0.3, labels={coluna: coluna}, title=titulo)

    fig.update_traces(textfont_color='black', textinfo='percent+label', textfont_size=14)
    fig.update_layout(
        showlegend=False,
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=22, color='white')),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        font=dict(color='white')  
    )

    return fig

def bar_hue_plot(df: pd.DataFrame, x_axis: str, y_axis: str, cor: str, titulo: str, modo: str = 'group', largura: int = 700):
    """
    Recebe um dataframe para fazer a plotagem dos dados.
    
    Parâmetros:
    - df: dataframe com as informações
    - x_axis: nome da coluna do eixo X
    - y_axis: nome da coluna do eixo Y
    - cor: nome da cor
    - titulo: título desejado
    - modo: modo das barras
    - largura: largura do gráfico

    Retorna:
    - Gráfico de dispersão
    """

    color_map = {
        'até 20 anos': '#ADD8E6',
        'entre 21 a 30 anos': '#3e75a8',
        'entre 31 a 40 anos': '#555b6e',
        'entre 41 a 50 anos': '#577590',
        'entre 51 a 60 anos': '#8e9aaf',
        'entre 61 a 70 anos': '#d3d3d3', 
        'mais de 70 anos': '#403d39',
        'Nao Informada': '#0d3b66',
    }  
    fig = px.bar(df, x=x_axis, y=y_axis, color=cor,
                 barmode=modo, title=titulo,
                 color_discrete_map=color_map)
    fig.update_traces(
        texttemplate='%{y}', textposition='outside',
        marker_line_width=1.5,
        textfont=dict(size=18, color='white')  # Ajusta o tamanho e a cor da fonte dos valores acima das barras
    )
    fig.update_layout(
        showlegend=True,
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5,
            font=dict(size=22, color='white'),
        ),
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=22, color='white')),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        width=largura,
        height=600,
        xaxis=dict(
            title=dict(text='', font=dict(size=22, color='white')),  
            tickfont=dict(size=22, color='white') 
        )
    )

    return fig

def bar_plot(df: pd.DataFrame, x_axis: str, y_axis: str, titulo: str, largura: int = 700):
    """
    Recebe um dataframe para fazer a plotagem dos dados.
    
    Parâmetros:
    - df: dataframe com as informações
    - x_axis: nome da coluna do eixo X
    - y_axis: nome da coluna do eixo Y
    - titulo: título desejado
    - largura: largura do gráfico

    Retorna:
    - Gráfico de barras
    """

    fig = px.bar(df[0:6], x=x_axis, y=y_axis)
    fig.update_xaxes(tickfont=dict(size=15))
    fig.update_traces(
        texttemplate='%{y}', textposition='outside',
        marker_line_width=1.5,
        textfont=dict(size=18, color='white')  # Ajusta o tamanho e a cor da fonte dos valores acima das barras
    )
    fig.update_layout(
        showlegend=True,
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=22, color='white'),
        ),
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=22, color='white')),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        width=largura,
        height=600,
        xaxis=dict(
            title=dict(text='', font=dict(size=22, color='white')),  
            tickfont=dict(size=22, color='white') 
        )
    )

    return fig
