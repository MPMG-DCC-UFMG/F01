# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import numpy as np

path_api = 'Governador Valadares/compare_data/servidores_api.csv'
path_portal = 'Governador Valadares/compare_data/servidores-por-cargos.csv'

def convert_date(df, column_name):
    
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    
    return df

def filter_by_date(df, column_name, min_date='2021-01-01', max_date='2021-02-01'):
    
    df = df.loc[(df[column_name]>= min_date) & (df[column_name] < max_date)]
    
    return df

def format_values(df, column_name):
    
    df[column_name] = df[column_name].str.replace("R", '', regex=True)
    df[column_name] = df[column_name].str.replace("$", '', regex=True)
    df[column_name] = df[column_name].str.replace(".", '', regex=True)
    df[column_name] = df[column_name].str.replace(",", '.', regex=True)
    df[column_name] = df[column_name].astype(float)
    
    return df


dados_api = pd.read_csv(path_api)
#data processing
dados_api = dados_api.loc[dados_api['DtCompetencia'] == '03/2021']
dados_api.drop(['DescServidor', 'DescUnidade', 'NumMatricula','DescFuncao', 'VlBase', 'VlDesconto', 'DtCompetencia', 'VlLiquido'], axis=1 , inplace=True)
dados_api['DescCargo'] = dados_api['DescCargo'].str.lower()
dados_api.columns = ['Cargo/Função', 'Valor']
# dados_api.sort_values(by='Cargo/Função', inplace = True)

dados_api = dados_api.groupby('Cargo/Função')['Valor'].sum()
dados_api = dados_api.apply(lambda x: round(x,2))
# dados_api['Valor'] = dados_api['Valor'].astype(float)
dados_api = dados_api.reset_index()

dados_api.to_csv("Governador Valadares/compare_data/dados_api.csv", index = True)
print(dados_api)


dados_portal = pd.read_csv(path_portal)
#data processing
dados_portal['Cargo/Função'] = dados_portal['Cargo/Função'].str.lower()
format_values(dados_portal,'Valor')
dados_portal.sort_values(by='Cargo/Função', inplace = True)
# dados_portal = dados_portal.groupby('Cargo/Função')['Valor'].sum().reset_index()
# dados_portal['Valor'] = dados_portal['Valor'].astype(float)
dados_portal.to_csv("Governador Valadares/compare_data/dados_portal.csv", index = True)
print(dados_portal)

# Merge
merge = pd.merge(dados_api, dados_portal, how = 'inner', on = ['Cargo/Função', 'Valor'])
merge.to_csv("Governador Valadares/compare_data/merge.csv", index = True)
print(merge)


