# Empenhos

from utils import indexing
import numpy as np
import sys
from utils import checker
from utils import path_functions
import pandas as pd
import numpy as np
from utils import read

sys.path.insert(1, '../')

from itertools import count
import pandas as pd
from utils import html_to_csv
import numpy as np
from utils import checker
from utils import path_functions

def get_df(files, ttype):
    df_final = pd.DataFrame()
    for key, values in files.items():
        if key in ttype:
            df = html_to_csv.load_and_convert_files(paths=values, format_type=key)
            df_final = pd.concat([df, df_final], axis=0, ignore_index=True)
    return df_final

# DESPESAS = {
#     'numero' : ['Número', 'Empenho', 'Empenho/ Processo'],
#     'descricao' : ['Unidade', 'Fornecedor','Ação', 'Descrição', 'Tipo'],
#     'favorecido' : ['Favorecido', 'Credor'],
#     'valor' : ['Empenhado', 'Liquidado', 'Pago', 'Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 'Empenhado no período (R$)']
# }

def check_all_values_of_column(df, valor, typee='valor'):
    """
    Checked if a column of a dataframe has more of half of values valid.

    Parameters
    ----------
    df : dataframe
        value to be verified
    valor : 
    type  : 'valor', 'data' or 'ano'
        
    Returns
    -------
    Boolean
        If value is valid, return true else false.
    """
    
    if typee == 'valor':
        vfunc = np.vectorize(checker.check_value)
    if typee == 'data':
            vfunc = np.vectorize(checker.check_date)
    if typee == 'ano':
        vfunc = np.vectorize(checker.check_year)
    if typee == 'text':
        vfunc = np.vectorize(checker.check_description)

    valid = []
    df['isvalid'] = False    

    if not len(df):
        return df, False

    if valor in df.columns:
        if typee == 'valor':
            if df[valor].dtypes != float:
                df = checker.format_values(df, valor)
        df['isvalid'] =  vfunc(df[valor])
        valid.append(df['isvalid'].sum())

    isvalid = False
    for c in valid:
        if c > (len(df.index)/2):
            isvalid = True

    return df, isvalid

class Empenhos:

    def __init__(self, files, ttype):

        files = path_functions.filter_paths(files, words=['empenhos'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files

        self.df = get_df(self.files, ttype)

    # Número
    def predict_numero(self, keyword_check):
        # Cheking valor
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='valor')
        return isvalid, result

    # Valor
    def predict_valor(self, keyword_check):
        # Cheking valor
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='valor')
        return isvalid, result

    # Data
    def predict_data(self, keyword_check):
        # Cheking data
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='data')
        return isvalid, result
    
    # Favorecido
    def predict_favorecido(self, keyword_check):
        # Cheking favorecido
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='text')
        return isvalid, result
    
    # Descrição
    def predict_descricao(self, keyword_check):
        # Cheking descricao
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='text')
        return isvalid, result
        
    def explain(self, result, column_name, description):
        result = f"""
        Quantidade de entradas encontradas e analizadas: {len(result[column_name])} 
        Quantidade de entradas que possuem {description} do empenho válido: {sum(result['isvalid'])}
        """
        return result