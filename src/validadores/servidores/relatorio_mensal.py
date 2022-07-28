
from utils import indexing
from utils import path_functions
from utils.file_to_df import get_df
from utils.check_df import check_all_values_of_column
from utils.check_df import search_in_column

class ValidadorRelatorioMensal:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        # print(self.df)

    def predict_agentes_politicos(self):
        result = self.df
        result['isvalid'] = False
        return False, result

    
    def predict(self):

        resultados = {
            'agentes_politicos': {},
        }

        # Agentes políticos
        isvalid, result = self.predict_agentes_politicos()
        result_explain = self.explain(result, 'agentes políticos')
        resultados['agentes_politicos']['predict'] = isvalid
        resultados['agentes_politicos']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        try:
            result = f"""Quantidade de registros de {description} encontrados: {sum(result['isvalid'])}"""
            return result
        except KeyError:
            return "Não encontrado"