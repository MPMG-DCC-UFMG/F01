# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime


def convert_date(df, column_name):
    
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    
    return df


def filter_by_date(df, column_name, min_date='2021-01-01', max_date='2021-02-01'):
    
    df = df.loc[(df[column_name]>= min_date) & (df[column_name] < max_date)]
    
    return df


def format_values(df, column_name):
    
    df[column_name] = df[column_name].str.replace("R", '')
    df[column_name] = df[column_name].str.replace("$", '')
    df[column_name] = df[column_name].str.replace(".", '')
    df[column_name] = df[column_name].str.replace(",", '.')
    df[column_name] = df[column_name].astype(float)
    
    return df


dados_portal = pd.read_csv("../../Governador Valadares/dados-processados/receitas-por-dias.csv")
dados_api = pd.read_csv("../../Governador Valadares/API/orcamentaria/receitasdia.csv")

dados_portal = convert_date(df=dados_portal, column_name='Data da Arrecadação')
dados_portal = filter_by_date(df=dados_portal, column_name='Data da Arrecadação', min_date='2021-01-01', max_date='2021-02-01')
dados_portal = format_values(df=dados_portal, column_name='Valor')

dados_api = convert_date(df=dados_api, column_name='dtMovimento')
dados_api = filter_by_date(df=dados_api, column_name='dtMovimento', min_date='2021-01-01', max_date='2021-02-01')


dados_portal.loc[dados_portal['Elemento'] == '1.1.1.3.03.11.00']


dados_api.loc[dados_api['numReceita'] == '1.1.1.3.03.11.00']

