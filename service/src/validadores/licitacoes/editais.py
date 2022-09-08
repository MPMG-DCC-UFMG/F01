from utils import indexing
from utils import path_functions
from utils import path_functions
from utils.file_to_dataframe import get_df
from utils.check_df import check_all_values_of_column

class ValidadorEditais:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['licitacao'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_editais(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['edital'], typee='text')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'editais': {}
        }

        # Editais
        isvalid, result = self.predict_editais()
        result_explain = self.explain(result, 'edital')
        resultados['editais']['predict'] = isvalid
        resultados['editais']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        try:
            numero_de_entradas = len(result)
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} da licitação válido: {sum(result['isvalid'])}"""
        return result