# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import numpy as np

path_portal = 'Governador Valadares/compare_data/servidores-por-nomes.csv'
path_api = 'Governador Valadares/compare_data/servidores_api.csv'

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
dados_api.drop(['DescCargo', 'DescUnidade', 'VlBase', 'DtCompetencia', 'DescFuncao','VlDesconto','VlLiquido'], axis=1 , inplace=True)
print(dados_api.columns)
dados_api.columns = ['Matrícula', 'Nome', 'Valor']
dados_api['Nome'] = dados_api['Nome'].str.lower()
dados_api.sort_values(by=['Nome'], inplace = True)
dados_api.index = np.arange(0,7391,1)


dados_portal = pd.read_csv(path_portal)
#data processing
dados_portal.drop(['Unidade', 'Cargo/Função'], axis=1 , inplace=True)
format_values(dados_portal,'Valor')
dados_portal['Nome'] = dados_portal['Nome'].str.lower()
dados_portal.sort_values(by=['Nome'], inplace = True)
dados_portal.index = np.arange(0,6079,1)


# Names in api that are not on the portal
# only_api = dados_api.loc[~dados_api['Nome'].isin(dados_portal['Nome'])]
# print(only_api)

# Duplicate names in api
# duplicate_names_api = dados_api["Nome"].duplicated(keep=False)
# print(dados_api[duplicate_names_api])


# Duplicate names in portal
# duplicate_names_portal = dados_portal["Nome"].duplicated(keep=False)
# print(dados_portal[duplicate_names_portal])

merge1 = pd.merge(dados_api, dados_portal, how = 'inner')
print(merge1)
serie_nomes_duplicados_merge = merge1["Nome"].duplicated(keep=False)
# print(merge1[serie_nomes_duplicados_merge])

# dados_api.columns = ['Matrícula', 'OutroNome', 'Valor']

# merge2 = pd.merge(dados_api, dados_portal, how = 'inner')
# print(merge2)
# serie_nomes_duplicados_merge = merge2["Nome"].duplicated(keep=False)
# print(merge2[serie_nomes_duplicados_merge])

# only_2 = merge2.loc[~merge2['Nome'].isin(merge1['Nome'])]
# print(only_2)

# result = 6078 rows in merge  / 7391 api
result = 0.82



