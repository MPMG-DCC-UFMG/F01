import pandas as pd
import numpy as np

def convert_date(df, column_name):
    df[column_name] = [d.date() for d in df[column_name]]
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df
    

def filter_by_date(df, column_name, min_date='2005-01-01', max_date='2021-05-12'):
    df = df.loc[(df[column_name]>= pd.to_datetime(min_date).date()) & (df[column_name] <pd.to_datetime(max_date).date())]
    return df

def format_api_df(df):
    
    df = df.drop_duplicates()
    df = df.drop(['descUnidadePai'], axis = 1)
    
    cols = ['descUnidade', 'descTipo', 'descDescricao', 'descCompetencia', 'descResponsavel', 'descEmail', 'descHorario', 'enderecos']

    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
            .replace(r'\r+|\n+|\t+|\W', '', regex=True).replace(' ', '')
        )
        
    return df

def format_dump_df(df):
    df = df.drop_duplicates()
    cols = ['descUnidade', 'descTipo', 'descDescricao', 'descCompetencia', 'descResponsavel', 'descEmail', 'descHorario', 'enderecos']
    

    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
            .replace(r'\r+|\n+|\t+|\W', '', regex=True).replace(' ', '')
        )
        
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/organograma.csv")
    dados_api = pd.read_csv("Governador Valadares/API/organizacional/unidades.csv")   

    dados_portal = format_dump_df(dados_portal)
    dados_api = format_api_df(dados_api)

    
    dados_portal.to_csv('portalnovo.csv')

    # print(len(intersection_f(list(dados_api['enderecos']), list(dados_portal['enderecos'])))/len(list(dados_api['enderecos'])))

    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['descUnidade', 'descTipo', 'descDescricao', 'descCompetencia', 'descResponsavel', 'descEmail'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))

main()