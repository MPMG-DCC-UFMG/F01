# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import numpy as np

path_api = 'Governador Valadares/compare_data/servidores_api.csv'
path_portal = 'Governador Valadares/compare_data/servidores-por-unidades.csv'

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
dados_api.drop(['DescServidor', 'NumMatricula','DescFuncao','DescCargo', 'VlBase', 'VlDesconto', 'DtCompetencia', 'VlLiquido'], axis=1 , inplace=True)
dados_api.columns = ['Unidade', 'Valor']
dados_api['Unidade'] = dados_api['Unidade'].str.lower()
dados_api['Unidade'] = dados_api['Unidade'].str.replace("  | ", '', regex=True)
dados_api.sort_values(by='Unidade', inplace = True)

dados_api = dados_api.groupby('Unidade')['Valor'].sum()
dados_api = dados_api.apply(lambda x: round(x,2))
# dados_api['Valor'] = dados_api['Valor'].astype(float)
dados_api = dados_api.reset_index()

dados_api.to_csv("Governador Valadares/compare_data/dados_api.csv", index = True)
print(dados_api)


dados_portal = pd.read_csv(path_portal)
#data processing
dados_portal['Unidade'] = dados_portal['Unidade'].str.lower()
format_values(dados_portal,'Valor')
dados_portal['Unidade'] = dados_portal['Unidade'].str.replace("  | ", '', regex=True)

print(dados_portal)

# Merge
merge = pd.merge(dados_api, dados_portal, how = 'inner', on = ['Unidade', 'Valor'])
merge.to_csv("Governador Valadares/compare_data/merge.csv", index = True)
print(merge)


