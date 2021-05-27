import pandas as pd
from datetime import datetime


def convert_date(df, column_name):
    
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    
    return df


def filter_by_date(df, column_name, min_date='2021-01-01', max_date='2021-02-01'):
    
    df = df.loc[(df[column_name]>= min_date) & (df[column_name] <= max_date)]
    
    return df


def format_values(df, column_name):
    
    df[column_name] = df[column_name].str.replace("R", '')
    df[column_name] = df[column_name].str.replace("$", '')
    df[column_name] = df[column_name].str.replace(".", '')
    df[column_name] = df[column_name].str.replace(",", '.')
    df[column_name] = df[column_name].astype(float)
    
    return df

dados_portal = pd.read_csv("/content/despesas-empenho.csv")
dados_api = pd.read_csv("/content/empenhos14-21.csv")

dados1 = dados_portal
dados2 = dados_api

dados1 = convert_date(dados1, "Data")

dados1 = format_values(dados1,"Empenhado")
dados1 = format_values(dados1,"Liquidado")
dados1 = format_values(dados1,"Pago")

dados2 = convert_date(dados2,"DtEmpenho")

dados1 = filter_by_date(dados1,"Data",'2021-01-01','2021-03-31')
dados2 = filter_by_date(dados2, "DtEmpenho",'2021-01-01','2021-03-31')

dados1["Empenho"] = dados1["Empenho"].astype(int)

intersecao = dados2.merge(dados1,right_on=["Empenho","Empenhado","Data"],left_on=["NumEmpenho","VlEmpenho","DtEmpenho"])
print('Tamanho da Interseção: ', len(intersecao), ' Porcentagem intersecao/api : ', len(intersecao)/len(dados_api))
print('Diferença: ', max(len(dados1), len(dados2)) - len(intersecao))