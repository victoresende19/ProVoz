import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import nltk
import spacy.cli
from utils.data import data
from utils.preprocessing import pre_processing_topics
from utils.topic import normalize, lemanization, tfidf_processing
from utils.style import style
from utils.plots import pie_plot, bar_hue_plot, bar_plot

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=5)
def nlp_download():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')

nlp_download()

st.set_page_config(layout="wide", page_icon='🚨', page_title='ProVoz')
st.markdown(style(), unsafe_allow_html=True)

st.markdown("<h1 style='text-align: left; font-size:52px; color: white'>ProVoz</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align: left; font-size:16px'>Quando os consumidores brasileiros precisam reclamar de empresas, o primeiro passo é ir ao Procon e registrar uma reclamação. Explore o perfil do consumidor e o tópico mais reclamado por UF e faixa etária na plataforma ProVoz! A base de dados utilizada refere-se ao ano de 2016 e pode ser encontrada <a href='https://dados.mj.gov.br/dataset/cadastro-nacional-de-reclamacoes-fundamentadas-procons-sindec'>clicando aqui (Ministério da justiça - Sindec) </a>.<br>", unsafe_allow_html=True)
eda, topics = st.tabs(["Perfil do consumidor", "Tópicos com mais reclamações"])

df = data()
df = df[df['SexoConsumidor'] != 'N'].dropna(subset=['DescCNAEPrincipal'])

df_UF_top = df.copy()
top_5_products = df_UF_top['UF'].value_counts().nlargest(4).index
df_UF_top['UF'] = df_UF_top['UF'].apply(lambda x: x if x in top_5_products else 'Outros')
df_regiao_faixa = df.groupby(by=["Regiao", "FaixaEtariaConsumidor"]).size().reset_index(name="Count")

with eda:
    st.write('')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Quantidade de reclamações", f"{len(df):,}".replace(',', '.'))
    col2.metric("Reclamações não atendidas", f"{len(df[df['Atendida'] != 'S']):,}".replace(',', '.'))
    col3.metric("UF com mais reclamações", df['UF'].mode()[0])
    col4.metric("CNAE com mais reclamações", df['DescCNAEPrincipal'].mode()[0].capitalize())

    st.write('')
    st.write('')
    st.write('')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(pie_plot(df, 'SexoConsumidor', 'Reclamações por gênero (%)'), use_container_width=True)
    with col2:
        st.plotly_chart(pie_plot(df, 'Regiao', 'Reclamações por região (%)'), use_container_width=True)
    with col3:
        st.plotly_chart(pie_plot(df_UF_top, 'UF', 'Reclamações por UF (%)'), use_container_width=True)


    st.plotly_chart(bar_hue_plot(df_regiao_faixa, 'Regiao', 'Count', 'FaixaEtariaConsumidor', 'Reclamações por faixa etaria e região'), use_container_width=True)


with topics:
    with st.form(key='procon'):
        with st.expander("Faça filtros para encontrar os tópicos com mais reclamações", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                valuesUF = sorted(df['UF'].unique())
                optionUF = st.selectbox(label='UF', options=valuesUF, index=None, placeholder='Escolha uma opção')
            with col2:
                valuesFaixaEtaria = sorted(df['FaixaEtariaConsumidor'].unique())
                optionFaixaEtaria = st.selectbox(label='Faixa etária consumidor', options=valuesFaixaEtaria,  index=None, placeholder='Escolha uma opção')
            with col3:
                valuesGram = ['Uma', 'Duas']
                optionGram = st.selectbox(label='Quantidade palavras', options=valuesGram,  index=None, placeholder='Escolha uma opção')

        submit_button = st.form_submit_button(label='Encontrar tópicos mais reclamados 💥')

        if submit_button:
            if not any([optionUF, optionFaixaEtaria, optionGram]):
                st.table(df.head(5).reset_index(drop=True))
            else:
                df_processed = pre_processing_topics(df, optionUF, optionFaixaEtaria)
                sentences_normalized = normalize(df_processed)

                with st.spinner('Gerando os tópicos, aguarde...'):
                    preprocessed_sentences = [lemanization(sentence) for sentence in sentences_normalized['processed'].to_list()]
                    gram_map = {'Uma': 1, 'Duas': 2}

                    try:
                        gram_df = tfidf_processing(preprocessed_sentences, gram_map[optionGram])
                    
                        st.write('')
                        st.write('')
                        st.markdown(f"<h2 style='text-align: center; font-size:32px; color: white'>Os tópicos mais reclamados no estado <strong>{optionUF}</strong> e clientes <strong>{optionFaixaEtaria}</strong></h2><br>", unsafe_allow_html=True)
                        st.write('')
                
                        for n_topic, termo in enumerate(gram_df[0:5].termo.values):
                            st.markdown(f"<p style='text-align: justify; max-width: 300px; margin: auto; font-size: 32px;'>Tópico {n_topic + 1} - {termo.capitalize()}<br></p>", unsafe_allow_html=True)
                    
                    except ValueError as e:
                        st.error('🚨 Não foi possível identificar tópicos de reclamações para esse filtro. Tente outra combinação 🚨')
