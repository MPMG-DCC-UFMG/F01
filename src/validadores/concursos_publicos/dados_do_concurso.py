from utils import indexing
from utils import path_functions
from utils.file_to_dataframe import get_df
from utils.check_df import check_all_values_of_column, search_in_column

class ValidadorDadosDoConcurso:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['concursopublico'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_status(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['status'], typee='text')
        return isvalid, result

    def predict_resultado(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['resultado'], typee='text')
        return isvalid, result
    
    def predict_atos_de_nomeacao(self):
        keywords = ["nomeação"]
        result = search_in_column(self.df, self.keywords['atos_de_nomeacao'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result
    
    def predict(self):

        resultados = {
            'status': {},
            'resultado': {},
            'atos_de_nomeacao': {},
        }

        # Status
        isvalid, result = self.predict_status()
        result_explain = self.explain(result, f"\"{self.keywords['status']}\"")
        resultados['status']['predict'] = isvalid
        resultados['status']['explain'] = result_explain

        # Resultado
        isvalid, result = self.predict_resultado()
        result_explain = self.explain(result, f"\"{self.keywords['resultado']}\"")
        resultados['resultado']['predict'] = isvalid
        resultados['resultado']['explain'] = result_explain

        # Atos de nomeação
        isvalid, result = self.predict_atos_de_nomeacao()
        result_explain = self.explain(result, f"nomeação no campo \"{self.keywords['atos_de_nomeacao']}\"")
        resultados['atos_de_nomeacao']['predict'] = isvalid
        resultados['atos_de_nomeacao']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade de entradas encontradas e analizadas que possuem {description}: {sum(result['isvalid'])}"""
        return result