# Empenhos

from utils import indexing
import pandas as pd
from utils import html_to_csv
import numpy as np
from utils import checker
from utils import path_functions
import pandas as pd
import numpy as np
from ..base import Validador

# def list_to_text(soup):

#     type = []
#     text = []
#     try:
#         for i in soup.find('div', { 'id' : 'detalhes' }).findAll('li'):
#             info = i.get_text().split(': ')
        
#             if len(info) == 2:
#                 type.append(info[0].lower().replace('\n', ''))
#                 text.append(info[1])
#             elif len(info) == 1:
#                 type.append(info[0].lower().replace('\n', ''))
#                 text.append('')

#         df = pd.DataFrame([text], columns=type)

#     except AttributeError:
#         df = pd.DataFrame()
#         pass

#     return df

# def convert_html_table(soup):
#     type = 'None'
#     try:
#         # Deleting <tfoot> element 
#         if soup.tfoot:
#             soup.tfoot.extract()
#         df = pd.read_html(str(soup.table))[0]
#         type = 'table'
#     except ValueError:
#         df = list_to_text(soup)
#         type = 'list'
    
#     return df, type

# def convert_to_df(all_files):

#     """
#     Recebe arquivos html, concatena as tabelas e retorna em um dataframe
#     """

#     list_df = []
#     for file in all_files:

#         soup = read.read_html(file)
#         df, _ = convert_html_table(soup)
#         list_df.append(df)

#     df = pd.DataFrame()
#     if(len(list_df)):
#         df = pd.concat(list_df)
#         df = df.drop_duplicates()

#     return df


def get_df(files, ttype):
    df_final = pd.DataFrame()
    for key, values in files.items():
        if key in ttype:
            df = html_to_csv.load_and_convert_files(paths=values, format_type=key)
            df_final = pd.concat([df, df_final], axis=0, ignore_index=True)
    return df_final


def add_in_dict(output, item, isvalid, result_explain):
    output[item]['predict'] = isvalid
    output[item]['explain'] = result_explain
    return output

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

class ValidadorPagamentos(Validador):

    def __init__(self, job_name, keywords):

        #Serch files
        self.keywords = keywords

        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['pagamentos'])
        files = path_functions.agg_paths_by_type(files)

        self.files = files

        ttype = keywords['types']
        self.df = get_df(self.files, ttype)

    # Valor
    def predict_valor(self, keyword_check):
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='valor')
        return isvalid, result

    # Data
    def predict_data(self, keyword_check):
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='data')
        return isvalid, result

    # Favorecido
    def predict_favorecido(self, keyword_check):
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='text')
        return isvalid, result

    # Empenho de referencia
    def predict_empenho_referencia(self, keyword_check):
        result, isvalid = check_all_values_of_column(self.df, keyword_check, typee='text')
        return isvalid, result

    def predict(self):

        output = {
            'pagamentos_valor': {},
            'pagamentos_data': {},
            'pagamentos_favorecido': {},
            'pagamentos_empenho_de_referencia': {},
        }

        # Valor
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor'], typee='text')
        explain = self.explain(result, self.keywords['valor'], 'a descrição')
        output = add_in_dict(output, 'pagamentos_valor', isvalid, explain)

        # Data
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data'], typee='text')
        explain = self.explain(result, self.keywords['data'], 'a descrição')
        output = add_in_dict(output, 'pagamentos_data', isvalid, explain)

        # Favorecido
        result, isvalid = check_all_values_of_column(self.df, self.keywords['favorecido'], typee='text')
        explain = self.explain(result, self.keywords['favorecido'], 'a descrição')
        output = add_in_dict(output, 'pagamentos_favorecido', isvalid, explain)

        # Empenho de referencia
        result, isvalid = check_all_values_of_column(self.df, self.keywords['empenho_de_referencia'], typee='text')
        explain = self.explain(result, self.keywords['empenho_de_referencia'], 'a descrição')
        output = add_in_dict(output, 'pagamentos_empenho_de_referencia', isvalid, explain)

        return output

    def explain(self, result, column_name, description):

            try:
                result = f"""
                Quantidade de entradas encontradas e analizadas: {len(result[column_name])} 
                Quantidade de entradas que possuem {description} do empenho válido: {sum(result['isvalid'])}
                """

            except KeyError:
                result = f"""
                Quantidade de entradas encontradas e analizadas: {0} 
                Quantidade de entradas que possuem {description} do empenho válido: {sum(result['isvalid'])}
                """

            return result
