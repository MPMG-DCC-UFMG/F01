import pandas as pd

def convert_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df


def filter_by_date(df, column_name, min_date='2013-01-01', max_date='2022-05-12'):
    df[column_name] = [d.date() for d in df[column_name]]
    df = df.loc[(df[column_name]>= pd.to_datetime(min_date).date()) & (df[column_name] < pd.to_datetime(max_date).date())]
    return df



def format_api_df(df):
    df = df.drop_duplicates()

    cols = ['descContaPublica', 'descPeriodo']
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    df.columns = ['Ano', 'Nome', 'Periodo', 'DataPublicacao']

    return df

def format_dump_df(df):
    df = df.drop_duplicates()

    cols = ['Nome', 'Periodo']
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/contas_publicas.csv")
    dados_api = pd.read_csv("Governador Valadares/API/legislacao-contas-publicas/contaspublicas.csv")   

    dados_portal = convert_date(df=dados_portal, column_name='DataPublicacao')
    dados_portal = format_dump_df(dados_portal)
    dados_api = convert_date(df=dados_api, column_name='dtPublicacao')
    dados_api = format_api_df(dados_api)
    

    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['Nome', 'Ano', 'Periodo','DataPublicacao'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))

main()