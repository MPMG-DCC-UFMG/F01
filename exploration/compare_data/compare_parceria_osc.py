import pandas as pd

def convert_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    return df


def filter_by_date(df, column_name, min_date='2018-01-01', max_date='2021-05-12'):
    df[column_name] = [d.date() for d in df[column_name]]
    df = df.loc[(df[column_name]>= pd.to_datetime(min_date).date()) & (df[column_name] <pd.to_datetime(max_date).date())]
    return df


def format_api_df(df):
    df = df.drop_duplicates()
    df = df.drop(['dtInicio', 'descObjeto','vlTotalParceria', 'descSituacao', 'descPrazoAnalise', 'dtLimite', 
    'descPeriodo', 'numAnoPrevisto','liberacaoRecursos', 'equipes', 'anexos', 'prestacaoContas', 'aditivos'], axis = 1)
    df['desUnidade'] = df['desUnidade'].str.split('Secretário', 1).str[0]

    cols = ['descTipoInstrumento', 'desUnidade']    
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    df.columns = ['Ano Instrumento', 'Numero Instrumento', 'Data de assinatura', 'Instrumento', 'Unidades', 'Fim da vigência']
    
    return df

def format_dump_df(df):
    df = df.drop_duplicates()
    temp = df['Instrumento'].str.split(' -')
    df['Instrumento'] = temp.str[0]
    temp = temp.str[1].str.split('/')
    df['Numero Instrumento'] = temp.str[0].astype(int)
    df['Ano Instrumento'] = temp.str[1].astype(int)

    cols = ['Instrumento', 'Unidades', 'Entidade']

    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/parcerias-com-osc.csv")
    dados_api = pd.read_csv("Governador Valadares/API/contratos-parcerias-licitacoes/parceriaosc.csv")   
    
    dados_portal = convert_date(df=dados_portal, column_name='Data de assinatura')
    dados_portal = convert_date(df=dados_portal, column_name='Fim da vigência')
    dados_portal = filter_by_date(df=dados_portal, column_name='Data de assinatura')
    dados_portal = format_dump_df(dados_portal)
    
    dados_api = convert_date(df=dados_api, column_name='dtAssinatura')
    dados_api = convert_date(df=dados_api, column_name='dtFinal')
    dados_api = filter_by_date(df=dados_api, column_name='dtAssinatura')
    dados_api = format_api_df(dados_api)
    
    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['Ano Instrumento', 'Numero Instrumento', 'Instrumento', 'Data de assinatura', 'Unidades', 'Fim da vigência'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))
main()