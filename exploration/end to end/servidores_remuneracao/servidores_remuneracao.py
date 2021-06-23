import os
import pandas as pd
import numpy as np
import datetime

from utils import table_to_csv
from utils.preprocess import format_values
from utils import checker
import constant

import warnings
warnings.filterwarnings("ignore")

path = "./Governador Valadares/API/recursos-humanos/servidores/servidores.csv"

def explain(data):
    print("O Validador analisou as colunas com tipos chaves",data,
        "\n O valor de retorno é True se as colunas possuem conteúdos validos e False caso contrário.")

def get_folders(name, folders):
    
    despesas = []
    for folder in folders:
    
        if folder.find(name) != -1:
            despesas.append(folder)
            
    return despesas

def check_all_competencia(df, column='Competência'):
    
    vfunc = np.vectorize(checker.check_competencia)
    df[column + '_isvalid'] = vfunc(df[column])
    
    return df, df[column + '_isvalid'].all()

def check_all_dates(df, column='Data'):
    
    vfunc = np.vectorize(checker.check_date)
    df[column + '_isvalid'] = vfunc(df[column])
    
    return df, df[column + '_isvalid'].all()

def check_all_values(df, columns_name=['Remuneração','Descontos','Valor Líquido']):
    vfunc = np.vectorize(checker.check_value)
    valid = []
    
    for i in columns_name:
        if i in df.columns:
            if df[i].dtypes != float:
                df = format_values(df, i)
            df[i + '_isvalid'] =  vfunc(df[i])
            valid.append((i, df[i + '_isvalid'].all()))
    
    return df, any(valid)

def check_all_description(df, columns_name=["Nome", "Cargo", "Lotação", "Código Matrícula", 'Vínculo']):
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


def main_pagamentos():
    
    data = {}
    df = pd.read_csv(path)

    df, value_isvalid = check_all_values(df, columns_name=constant.PAGAMENTOS_SERVIDORES_API['valor'])
    df, description_isvalid = check_all_description(df, columns_name=constant.PAGAMENTOS_SERVIDORES_API['descricao'])
    if 'Data' in df.columns:
        df, date_isvalid = check_all_dates(df, column='Data')
    elif 'Ano' in df.columns:
        df, date_isvalid = check_all_year(df, column='Ano')
    elif 'DtCompetencia' in df.columns:
        df, date_isvalid = check_all_competencia(df, column='DtCompetencia')

    data = {"date": date_isvalid, 'value': value_isvalid, 'description': description_isvalid}
    aux = pd.DataFrame(list(data.items()))
    result = pd.concat([aux.drop([1], axis=1), aux[1].apply(pd.Series)], axis=1)
    explain(data)
    return result


df = main_pagamentos()

print(df)
