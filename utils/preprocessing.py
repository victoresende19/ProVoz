import pandas as pd

def pre_processing_topics(df: pd.DataFrame, optionUF: str, optionFaixaEtaria: str) -> pd.DataFrame:
    """
    Faz o pre processamento dos dados

    Recebe:
        df: dataframe com os dados
    Retorna:
        df: dados após o processamento
    """

    df = df[~df['DescricaoProblema'].isna()]
    df = df[~df['DescricaoProblema'].str.isdigit()]
    df = df[df['DescricaoProblema'].apply(lambda x: len(x.split())) >= 4]
    df = df[(df['UF'] == optionUF) & (df['FaixaEtariaConsumidor'] == optionFaixaEtaria)]
    df = df[df['Atendida'] == 'N']
    return df