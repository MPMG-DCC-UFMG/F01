import pandas as pd

def convert_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df


def filter_by_date(df, column_name, min_date='2021-01-01', max_date='2021-05-12'):
    df = df.loc[(df[column_name]>= min_date) & (df[column_name] < max_date)]
    return df


def format_api_df(df):
    df.drop_duplicates()
    df = df.drop(['numExercicio', 'numOrdem', 'numExtra', 'tpExtra'], axis = 1)
    
    df[df.select_dtypes(include=[object]).columns] = df[df.select_dtypes(include=[object]).columns].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    df.columns = ['Data', 'Conta', 'Fornecedor', 'Valor']
    
    return df

def format_dump_df(df):
    df.drop_duplicates()
    df['Valor'] = df['Valor'].map(lambda x: x.lstrip('R$ '))
    df['Conta'] = df['Conta'].str.replace(r'\d+', '', regex = True)

    df[df.select_dtypes(include=[object]).columns] = df[df.select_dtypes(include=[object]).columns].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())

    return df

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/parcerias-com-osc.csv")
    dados_api = pd.read_csv("Governador Valadares/API/contratos-parcerias-licitacoes/parceriaosc.csv")   
    
    #dados_portal = convert_date(df=dados_portal, column_name='Data de assinatura')
    #dados_portal = filter_by_date(df=dados_portal, column_name='Data')
    #dados_portal = format_dump_df(dados_portal)
    #dados_api = convert_date(df=dados_api, column_name='dtMovimento')
    #dados_api = filter_by_date(df=dados_api, column_name='dtMovimento')
    #dados_api = format_api_df(dados_api)

    print(dados_api.columns)
    print(dados_portal.columns)
    """ intersection = pd.merge(dados_portal, dados_api, how ='inner', on =)
    print(intersection)
    print('Size of intersecion: ', len(intersection.index), ' Percentage of intersection/api data: ', len(intersection.index)/len(dados_api.index))
     """
main()