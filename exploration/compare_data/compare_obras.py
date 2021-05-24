import pandas as pd

def convert_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df


def filter_by_date(df, column_name, min_date='2013-01-01', max_date='2022-12-31'):
    df[column_name] = [d.date() for d in df[column_name]]
    df = df.loc[(df[column_name]>= pd.to_datetime(min_date).date()) & (df[column_name] < pd.to_datetime(max_date).date())]
    return df


def format_api_df(df):
    df = df.drop_duplicates()
    df = df.drop(['descUnidade','descExecucao', 'descAtendTipo', 'vlPrevisto', 'vlLicitado', 
    'vlPago', 'descRespTec', 'contratos', 'relacionadas', 'licitacoes'], axis = 1)

    cols = ['descObra', 'descTipo', 'descSituacao']    
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    df.columns = ['Nome', 'Tipo', 'Situacao', 'Data Inicio', 'Data Termino']
    
    return df

def format_dump_df(df):
    df = df.drop_duplicates()
    
    df['Tipo'] = df['Tipo'].str.split(': ', 1).str[1]
    df['Situacao'] = df['Situacao'].str.split(': ', 1).str[1]
    df['Data Inicio'] = df['Data Inicio'].str.split(': ', 1).str[1]
    df['Data Termino'] = df['Data Termino'].str.split(': ', 1).str[1]
    
    cols = ['Nome', 'Tipo', 'Situacao']
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/obras.csv")
    dados_api = pd.read_csv("Governador Valadares/API/obras/obras.csv")   
    
    dados_portal = format_dump_df(dados_portal)
    dados_portal = convert_date(df=dados_portal, column_name='Data Inicio')
    dados_portal = convert_date(df=dados_portal, column_name='Data Termino')

    dados_api = convert_date(df=dados_api, column_name='dtInicio')
    dados_api = convert_date(df=dados_api, column_name='dtFim')
    dados_api = format_api_df(dados_api)

    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['Nome', 'Tipo', 'Situacao', 'Data Inicio', 'Data Termino'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))
main()