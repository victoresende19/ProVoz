import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import requests
import streamlit as st

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=100)
def data(type):
    
    if type == 'zip':
        url = "http://dados.mj.gov.br/dataset/8ff7032a-d6db-452b-89f1-d860eb6965ff/resource/4d055554-0595-47ce-b3d4-97c11f33e143/download/reclamacoes-fundamentadas-sindec-2016v2.zip"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            zip_content = BytesIO(response.content)
            
            with ZipFile(zip_content) as z:
                with z.open('reclamacoes-fundamentadas-sindec-2016_v2.csv') as f:
                    return pd.read_csv(f, delimiter=';')
    else:
        return pd.read_csv('http://dados.mj.gov.br/dataset/8ff7032a-d6db-452b-89f1-d860eb6965ff/resource/bc23b54c-18e7-4ed8-b7f5-205434ac5719/download/crf2022dados-abertos.csv') 