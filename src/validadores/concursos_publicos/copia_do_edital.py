from utils import indexing
from utils import path_functions
from utils.file_to_df import get_df
from utils.check_df import check_all_values_of_column, search_in_column

class ValidadorCopiaDoEdital:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['concursopublico'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_copia_do_edital(self):

        keywords = ["edital"]
        result = search_in_column(self.df, self.keywords['copia_do_edital'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result
    
    def predict(self):

        resultados = {
            'copia_do_edital': {}
        }

        # Copia do edital
        isvalid, result = self.predict_copia_do_edital()
        result_explain = self.explain(result, f"\"{self.keywords['copia_do_edital']}\"")
        resultados['copia_do_edital']['predict'] = isvalid
        resultados['copia_do_edital']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade diferente de entradas encontradas e analizadas que possuem \"edital\" no campo {description}: {sum(result['isvalid'])}"""
        return result