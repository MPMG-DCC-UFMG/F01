import numpy as np
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.file_to_dataframe import get_df

class ValidadorEstruturaOrganizacional:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['estrutura_organizacional'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_estrutura_organizacional(self):

        num_arquivos = len(self.files['pdf'])
        if num_arquivos > 0:
            isvalid = True
        else: isvalid = False
         
        result = num_arquivos
        return isvalid, result
    
    def predict(self):

        resultados = {
            'estrutura_organizacional': {},
        }

        # Endereço
        isvalid, result = self.predict_estrutura_organizacional()
        result_explain = self.explain(result)
        resultados['estrutura_organizacional']['predict'] = isvalid
        resultados['estrutura_organizacional']['explain'] = result_explain

        return resultados
        
    def explain(self, result):
        result = f"""Foram encontrados {result} arquivos coletados sobre a estrutura organizacinal do municipio."""
        return result