import numpy as np
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.file_to_dataframe import get_df

class ValidadorRegistroDasCompetencias:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['registro_de_competencias'])
        self.files = path_functions.agg_paths_by_type(files)
        print(self.files)
        self.df = get_df(self.files, keywords['types'])

    def predict_registro_das_competencias(self):

        num_arquivos = len(self.files['pdf'])
        if num_arquivos > 0:
            isvalid = True
        else: isvalid = False
         
        result = num_arquivos
        return isvalid, result
    
    def predict(self):

        resultados = {
            'registro_das_competencias': {},
        }

        # registro_das_competencias
        isvalid, result = self.predict_registro_das_competencias()
        result_explain = self.explain(result)
        resultados['registro_das_competencias']['predict'] = isvalid
        resultados['registro_das_competencias']['explain'] = result_explain

        return resultados
        
    def explain(self, result):
        result = f"""Foram encontrados {result} arquivos coletados sobre a estrutura organizacinal do municipio."""
        return result