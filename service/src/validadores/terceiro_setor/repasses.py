from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorRepasses:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['terceiro_setor'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    # Origem
    def predict_origem(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['origem'], typee='text')
        return isvalid, result
    
    # Valor
    def predict_valor(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor'], typee='text')
        return isvalid, result

    # Data
    def predict_data(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data'], typee='text')
        return isvalid, result

    
    def predict(self):

        resultados = {
            'origem': {},
            'valor': {},
            'data': {},
        }

        # Origem
        isvalid, result = self.predict_origem()
        result_explain = self.explain(result, 'origem')
        resultados['origem']['predict'] = isvalid
        resultados['origem']['explain'] = result_explain

        # Valor
        isvalid, result = self.predict_valor()
        result_explain = self.explain(result, 'valor')
        resultados['valor']['predict'] = isvalid
        resultados['valor']['explain'] = result_explain

        # Data
        isvalid, result = self.predict_data()
        result_explain = self.explain(result, 'data')
        resultados['data']['predict'] = isvalid
        resultados['data']['explain'] = result_explain
        

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade de entradas encontradas e que possuem o campo {description} do repasse válido: {sum(result['isvalid'])}"""
        return result