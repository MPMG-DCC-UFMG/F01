import pandas as pd

def format_api_df(df):
    df = df.drop_duplicates()
    df = df.drop(['descTaxa','descUrl'], axis = 1)

    cols = ['descCategoria', 'descUnidade', 'descGuiaServ','descExigencia','descDocumento']
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    return df

def format_dump_df(df):
    df = df.drop_duplicates()

    df['descCategoria'] = df['descCategoria'].str.replace('Categoria: ', '')
    df['descUnidade'] = df['descUnidade'].str.replace('Unidade: ', '')
    
    cols = ['descCategoria', 'descUnidade', 'descGuiaServ','descExigencia','descDocumento','descricao']
    df[cols] = df[cols].apply( lambda x: 
        x.str.normalize('NFKD').str.replace(',', '').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower())
    
    return df

def intersection_f(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def main():
    dados_portal = pd.read_csv("Governador Valadares/dados-processados/servicos.csv")
    dados_api = pd.read_csv("Governador Valadares/API/organizacional/guiaservicos.csv")   
    
    dados_portal = format_dump_df(dados_portal)
    dados_api = format_api_df(dados_api)

    intersection = pd.merge(dados_portal, dados_api, how ='inner', on = ['descCategoria', 'descUnidade', 'descGuiaServ'])
    print('Size of intersecion: ', len(intersection), ' Percentage of intersection/api data: ', len(intersection)/len(dados_api))
    print('Diff: ', max(len(dados_portal), len(dados_api)) - len(intersection))

main()