# Empenhos

from utils import indexing
from utils.file_to_dataframe import get_df
from utils.check_df import check_all_values_of_column
from utils import path_functions
from ..base import Validador

class ValidadorPagamentos(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['pagamentos'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files
        self.df = get_df(self.files, keywords['types'])

    # Valor
    def predict_valor(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor'], typee='valor')
        return isvalid, result

    # Data
    def predict_data(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data'], typee='data')
        return isvalid, result

    # Favorecido
    def predict_favorecido(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['favorecido'], typee='text')
        return isvalid, result

    # Empenho de referencia
    def predict_empenho_referencia(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['empenho_de_referencia'], typee='text')
        return isvalid, result

    def predict(self):

        resultados_pagamentos = {
            'valor': {},
            'data': {},
            'favorecido': {},
            'empenho_de_referencia': {},
        }

        # Valor
        isvalid, result = self.predict_valor()
        result_explain = self.explain(result, self.keywords['valor'], 'o valor')
        resultados_pagamentos['valor']['predict'] = isvalid
        resultados_pagamentos['valor']['explain'] = result_explain

        # Data
        isvalid, result = self.predict_data()
        result_explain = self.explain(result, self.keywords['data'], 'a data')
        resultados_pagamentos['data']['predict'] = isvalid
        resultados_pagamentos['data']['explain'] = result_explain

        # Favorecido
        isvalid, result = self.predict_favorecido()
        result_explain = self.explain(result, self.keywords['favorecido'], 'o favorecido')
        resultados_pagamentos['favorecido']['predict'] = isvalid
        resultados_pagamentos['favorecido']['explain'] = result_explain

        # Empenho de referencia
        isvalid, result = self.predict_empenho_referencia()
        result_explain = self.explain(result, self.keywords['empenho_de_referencia'], 'o  empenho de referencia')
        resultados_pagamentos['empenho_de_referencia']['predict'] = isvalid
        resultados_pagamentos['empenho_de_referencia']['explain'] = result_explain

        return resultados_pagamentos

    def explain(self, result, column_name, description):
        try:
            result = f"""Quantidade de entradas encontradas e analizadas: {len(result[column_name])} 
            Quantidade de entradas que possuem {description} do pagamento válido: {sum(result['isvalid'])}"""

        except KeyError:
            result = f"""Quantidade de entradas encontradas e analizadas: {0} 
            Quantidade de entradas que possuem {description} do pagamento válido: {sum(result['isvalid'])}"""

        return result


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