# -*- coding: utf-8 -*-
# +
import os
import pandas as pd
import numpy as np
import datetime

import sys
sys.path.insert(1, '../')
# -

from utils import table_to_csv
from utils.preprocess import format_values
from utils import checker
import constant

import warnings
warnings.filterwarnings("ignore")


path = "../../../../Governador Valadares"


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


def main_despesas():
    
    data = {}

    folders = os.listdir(path)
    folders = get_folders("despesa", folders)

    for folder in folders:

        print(folder)

        all_files = os.listdir("{}/{}".format(path, folder))
        df = table_to_csv.convert(all_files, path, folder)

        df = df.loc[df[df.columns[0]] != "Total página Total geral"]

        if 'Data' in df.columns:
            df, date_isvalid = check_all_dates(df, column='Data')
        elif 'Ano' in df.columns:
            df, date_isvalid = check_all_year(df, column='Ano')

        df, value_isvalid = check_all_values(df, columns_name=constant.DESPESAS['valor'])
        df, description_isvalid = check_all_description(df, columns_name=constant.DESPESAS['descricao'])

        data[folder] = {"date": date_isvalid, 'value': value_isvalid, 'description': description_isvalid}

    aux = pd.DataFrame(list(data.items()))
    result = pd.concat([aux.drop([1], axis=1), aux[1].apply(pd.Series)], axis=1)
    
    return result


df = main_despesas()

df
