# Pagamentos
    # Valor
    # Data
    # Favorecido
    # Empenho de referência

# Empenhos
    # Número Valor Data Favorecido Descrição
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import datetime
import sys
from utils import checker
import pandas as pd
import numpy as np
import datetime
import warnings
from bs4 import BeautifulSoup
sys.path.insert(1, '../')
from utils import html_to_csv

#Textos de Planos e Leis Orçamentárias
LEIS_ORCAMENTARIAS = {
    'PLANO_PLURIANUAL': ['PPA - Plano Plurianual','Plano Plurianual'],
    'LEI_ORCAMENTARIA': ['Lei Orçamentária Anual','LOA - Lei Orçamentária Anual'],
    'LEI_DIRETRIZES':['Lei de Diretrizes Orçamentárias','LDO - Lei de Diretrizes Orçamentárias']
}
DESPESAS = {
    'descricao' : ["Favorecido", "Unidade", "Fornecedor","Ação", "Descrição", 'Tipo'],
    'valor' : ['Empenhado', 'Liquidado', 'Pago', "Valor Empenhado", "Valor Liquidado", "Valor Pago"]
}

warnings.filterwarnings("ignore")

path = '/home/asafe/GitHub/Coleta_C01/gv'

# -*- coding: utf-8 -*-

def format_values(df, column_name):
    
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].str.replace("R\$", '')
    df[column_name] = df[column_name].str.replace(".", '')
    df[column_name] = df[column_name].str.replace(",", '.')
    df[column_name] = df[column_name].astype(float)
    
    return df


def read_content(path, folder, file):
    
    page = open("{}/{}/{}".format(path, folder, file), encoding="utf8").read()
    soup = BeautifulSoup(page, features="lxml")
    
    return soup

def list_to_text(soup):

    type = []
    text = []
    try:
        for i in soup.find("div", { "id" : "detalhes" }).findAll('li'):
            info = i.get_text().split(": ")
        
            if len(info) == 2:
                type.append(info[0].lower().replace("\n", ''))
                text.append(info[1])
            elif len(info) == 1:
                type.append(info[0].lower().replace("\n", ''))
                text.append("")

        df = pd.DataFrame([text], columns=type)

    except AttributeError:
        df = pd.DataFrame()
        pass

    return df

def convert_html(soup):
    type = 'None'
    
    try:
        df = pd.read_html(str(soup.table))[0]
        type = 'table'
    except ValueError:
        df = list_to_text(soup)
        type = 'list'
    
    return df, type

def convert(all_files, path, folder):

    list_df = []
    for file in all_files:

        soup = read_content(path, folder, file)
        df, _ = convert_html(soup)
        list_df.append(df)

    print("*************")
    print(list_df)
    print(type(list_df[0]))
    print(type(list_df))
    df = pd.concat(list_df)
    df = df.drop_duplicates()
    
    return df

def convert_one_file(path):

    soup = BeautifulSoup(open(path), features="lxml")
    df = convert_html(soup)

    return df   


# ***************************


def get_folders(name, folders):
    
    despesas = []
    for folder in folders:
    
        if folder.find(name) != -1:
            despesas.append(folder)
            
    return despesas


def check_all_dates(df, column='Data'):
    
    vfunc = np.vectorize(checker.check_date)
    df[column + '_isvalid'] = vfunc(df[column])
    
    return df, df[column + '_isvalid'].all()

def check_all_values(df, columns_name=['Empenhado', 'Liquidado', 'Pago', "Valor Empenhado", "Valor Liquidado", "Valor Pago"]):

    vfunc = np.vectorize(checker.check_value)
    valid = []
    
    for i in columns_name:
        if i in df.columns:
            if df[i].dtypes != float:
                df = format_values(df, i)
            df[i + '_isvalid'] =  vfunc(df[i])
            valid.append((i, df[i + '_isvalid'].all()))
    
    return df, any(valid)

def check_all_description(df, columns_name=["Favorecido", "Unidade", "Fornecedor","Ação", "Descrição", 'Tipo']):

    vfunc = np.vectorize(checker.check_description)
    valid = []
    
    for i in columns_name:
        if i in df.columns:
            df[i + '_isvalid'] =  vfunc(df[i])
            valid.append((i, df[i + '_isvalid'].all()))
            
    return df, any(valid)

def check_all_year(df, column="Ano"):
    
    vfunc = np.vectorize(checker.check_year)
    df[column + '_isvalid'] =  vfunc(df[column])
    
    return df, df[column + '_isvalid'].all()


def check(folders, path, verbose=False):
    
    if verbose:
        print("Checking Values")
    
    data = {}
    
    for folder in folders:
    
        if verbose:
            print('-- {}'.format(folder))
            
        all_files = os.listdir("{}/{}".format(path, folder))
        print(all_files)
        print(path)
        print(folder)
        df = convert(all_files, path, folder)

        df = df.loc[df[df.columns[0]] != "Total página Total geral"]
        
        if 'Data' in df.columns:
            df, date_isvalid = check_all_dates(df, column='Data')
        elif 'Ano' in df.columns:
            df, date_isvalid = check_all_year(df, column='Ano')

        df, value_isvalid = check_all_values(df, columns_name=DESPESAS['valor'])
        df, description_isvalid = check_all_description(df, columns_name=DESPESAS['descricao'])
        
        data[folder] = {"date": date_isvalid, 'value': value_isvalid, 'description': description_isvalid}
        
    aux = pd.DataFrame(list(data.items()))
    print(aux)
    result = pd.concat([aux.drop([1], axis=1), aux[1].apply(pd.Series)], axis=1)
    
    return result


def search(path, keyword='despesa', verbose=False):
    
    if verbose:
        print("Search")
    
    folders = os.listdir(path)
    folders = get_folders(keyword, folders)
    
    return folders


def predict(path, keyword='despesa', verbose=False): 
    
    
    folders = search(path, keyword=keyword)

    if verbose:
        print("folders:", folders)

    df = check(folders, path, verbose)
    
    if verbose:
        print("Predict")
    
    prediction = df.date.all() and df.value.all()and df.description.all()
        
    return prediction, df


def explain(df):
    
    print("Os seguintes arquivos foram verificados:")
    for index, row in df.iterrows():
        print("{}:\n data: {}, valor: {}, descrição: {}".format(row[0], 
                                                                row['date'],
                                                                row['value'],
                                                                row['description']))


def main_despesas(keyword='despesa', verbose=True):
    
    prediction, df = predict(path, keyword=keyword, verbose=verbose)
    explain(df)

    # df = html_to_csv("/home/asafe/Github/Coleta_C01/gv/despesas-por-elementos", paths=['despesas-por-elementos_2.html'], type="html")

