from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorDadosDeParcerias:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['terceiro_setor'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    # Data de celebração
    def predict_data_de_celebracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data_de_celebracao'], typee='data')
        return isvalid, result
    
    # Objeto
    def predict_objeto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['objeto'], typee='text')
        return isvalid, result

    # Conveniados
    def predict_conveniados(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['conveniados'], typee='text')
        return isvalid, result

    # Aditivos
    def predict_aditivos(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['aditivos'], typee='valor')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'data_de_celebracao': {},
            'objeto': {},
            'conveniados': {},
            'aditivos': {}
        }

        # Data de celebração
        isvalid, result = self.predict_data_de_celebracao()
        result_explain = self.explain(result, 'data de celebração')
        resultados['data_de_celebracao']['predict'] = isvalid
        resultados['data_de_celebracao']['explain'] = result_explain

        # Objeto
        isvalid, result = self.predict_objeto()
        result_explain = self.explain(result, 'objeto')
        resultados['objeto']['predict'] = isvalid
        resultados['objeto']['explain'] = result_explain

        # Conveniados
        isvalid, result = self.predict_conveniados()
        result_explain = self.explain(result, 'conveniados')
        resultados['conveniados']['predict'] = isvalid
        resultados['conveniados']['explain'] = result_explain
        
        # Aditivos
        isvalid, result = self.predict_aditivos()
        result_explain = self.explain(result, 'aditivos')
        resultados['aditivos']['predict'] = isvalid
        resultados['aditivos']['explain'] = result_explain


        return resultados
        
    def explain(self, result, description):
        try:
            numero_de_entradas = len(result)
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} válido: {sum(result['isvalid'])}"""
        return result