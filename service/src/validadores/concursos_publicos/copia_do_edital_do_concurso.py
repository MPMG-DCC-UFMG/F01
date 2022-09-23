from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column, search_in_column

class ValidadorCopiaDoEdital:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['concursopublico'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_copia_do_edital_do_concurso(self):

        keywords = ["edital"]
        result = search_in_column(self.df, self.keywords['copia_do_edital_do_concurso'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result
    
    def predict(self):

        resultados = {
            'copia_do_edital_do_concurso': {}
        }

        # Copia do edital
        isvalid, result = self.predict_copia_do_edital_do_concurso()
        result_explain = self.explain(result, f"\"{self.keywords['copia_do_edital_do_concurso']}\"")
        resultados['copia_do_edital_do_concurso']['predict'] = isvalid
        resultados['copia_do_edital_do_concurso']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade diferente de entradas encontradas e analizadas que possuem \"edital\" no campo {description}: {sum(result['isvalid'])}"""
        return result