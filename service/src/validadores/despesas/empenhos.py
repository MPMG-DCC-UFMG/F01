from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorEmpenhos:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['empenhos'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files
        self.df = get_df(self.files, keywords['types'])

    # Número
    def predict_numero(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['numero'], typee='valor')
        return isvalid, result

    # Valor
    def predict_valor(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor'], typee='valor')
        return isvalid, result

    # Data
    def predict_data(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data'], typee='data')
        return isvalid, result
    
    # Favorecido
    def predict_favorecido(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['favorecido'], typee='text')
        return isvalid, result
    
    # Descrição
    def predict_descricao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['descricao'], typee='text')
        return isvalid, result

    def predict(self):

        resultados_empenhos = {
            'numero': {},
            'valor': {},
            'data': {},
            'favorecido': {},
            'descricao': {},
        }

        # Número
        isvalid, result = self.predict_numero()
        result_explain = self.explain(result, self.keywords['numero'], 'o numero')
        resultados_empenhos['numero']['predict'] = isvalid
        resultados_empenhos['valor']['explain'] = result_explain

        # Valor
        isvalid, result = self.predict_valor()
        result_explain = self.explain(result, self.keywords['valor'], 'o valor')
        resultados_empenhos['valor']['predict'] = isvalid
        resultados_empenhos['valor']['explain'] = result_explain

        # Data
        isvalid, result = self.predict_data()
        result_explain = self.explain(result, self.keywords['data'], 'a data')
        resultados_empenhos['data']['predict'] = isvalid
        resultados_empenhos['data']['explain'] = result_explain

        # Favorecido
        isvalid, result = self.predict_favorecido()
        result_explain = self.explain(result, self.keywords['favorecido'], 'o favorecido')
        resultados_empenhos['favorecido']['predict'] = isvalid
        resultados_empenhos['favorecido']['explain'] = result_explain

        # Descricao
        isvalid, result = self.predict_descricao()
        result_explain = self.explain(result, self.keywords['descricao'], 'a descricao')
        resultados_empenhos['descricao']['predict'] = isvalid
        resultados_empenhos['descricao']['explain'] = result_explain

        return resultados_empenhos
        
    def explain(self, result, column_name, description):
        result = f"""
        Quantidade de entradas encontradas e analizadas: {len(result[column_name])} 
        Quantidade de entradas que possuem {description} do empenho válido: {sum(result['isvalid'])}
        """
        return result