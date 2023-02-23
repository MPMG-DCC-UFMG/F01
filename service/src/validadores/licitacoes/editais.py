from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorEditais:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        try:
            filter_paths_key = keywords['filter_paths']
        except:
            filter_paths_key = "licitacao"
        files = path_functions.filter_paths(files, words=filter_paths_key)
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        print("self.columns:***", self.df.columns)

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