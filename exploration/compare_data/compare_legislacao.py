import pandas as pd
import numpy as np

def convert_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df
    

def filter_by_date(df, column_name, min_date='2005-01-01', max_date='2021-05-12'):
    df[column_name] = [d.date() for d in df[column_name]]
    df = df.loc[(df[column_name]>= pd.to_datetime(min_date).date()) & (df[column_name] <pd.to_datetime(max_date).date())]
    return df

def format_api_df(df):
    df["dtLegislacao"] = [d.date() for d in pd.to_datetime(df['dtLegislacao'])]
    df["dtAssinatura"] = [d.date() for d in pd.to_datetime(df['dtAssinatura'])]
    
    df = df.drop_duplicates()
    df = df.drop(['descResumo', 'stRevogada', 'assuntos', 'relacionadas'], axis = 1)
    

    df['descAssunto'] = df['descAssunto'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
    
    df.columns = ['Exercicio', 'Legislacao', 'DataPublicacao', 'DataAssinatura', 'Descricao']

    return df

def format_dump_df(df):
    df = df.drop_duplicates()

    df['numDecreto'] = df['numDecreto'].str.extract(r'(\d+.+$)')
    temp = df['numDecreto'].str.split('/')
    df['Legislacao'] = temp.str[0].fillna(0).astype(int)
    df['Exercicio'] = temp.str[1].fillna(0).astype(int)

    df['DataPublicacao'] = df['DataPublicacao'].str.replace('Publicado em ', '')
    df['DataAssinatura'] = df['DataAssinatura'].str.replace('Norma assinada em: ', '')

    df['Descricao'] = df['Descricao'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
    
    df = df.drop(['urlDecreto', 'numDecreto'], axis = 1)
    
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/legislacao.csv")
    dados_api = pd.read_csv("Governador Valadares/API/legislacao-contas-publicas/legislacoes.csv")   

    dados_portal = format_dump_df(dados_portal)
    dados_portal = convert_date(df=dados_portal, column_name='DataPublicacao')
    dados_portal = convert_date(df=dados_portal, column_name='DataAssinatura')
    dados_portal = filter_by_date(df=dados_portal, column_name='DataAssinatura')
    print(dados_portal['DataPublicacao'])
    dados_api = format_api_df(dados_api)
    dados_api = convert_date(df=dados_api, column_name='DataPublicacao')
    dados_api = convert_date(df=dados_api, column_name='DataAssinatura')
    dados_api = filter_by_date(df=dados_api, column_name='DataAssinatura')
    print(dados_api['DataPublicacao'])
    

    print(len(intersection_f(list(dados_api['Descricao']), list(dados_portal['Descricao'])))/len(list(dados_api['Descricao'])))

    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['Exercicio', 'Legislacao', 'Descricao'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))

main()