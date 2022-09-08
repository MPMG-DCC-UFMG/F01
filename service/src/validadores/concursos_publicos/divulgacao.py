from utils import indexing
from utils import path_functions
from utils.file_to_dataframe import get_df
from utils.check_df import search_in_column

class ValidadorDivulgacaoRecursosDecisoes:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['concursopublico'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_divulgacao_dos_recursos_e_respectivas_decisoes(self):

        keywords = self.keywords['value']
        result = search_in_column(self.df, self.keywords['column'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result
    
    def predict(self):

        resultados = {
            'divulgacao_dos_recursos_e_respectivas_decisoes': {}
        }

        # Divulgação dos recursos e respectivas decisões
        isvalid, result = self.predict_divulgacao_dos_recursos_e_respectivas_decisoes()
        result_explain = self.explain(result, f"\"{self.keywords['column']}\"")
        resultados['divulgacao_dos_recursos_e_respectivas_decisoes']['predict'] = isvalid
        resultados['divulgacao_dos_recursos_e_respectivas_decisoes']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade diferente de entradas encontradas e analizadas que possuem referencia a recursos ou respectivas decisões no campo {description}: {sum(result['isvalid'])}"""
        return result