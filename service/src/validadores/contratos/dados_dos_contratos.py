from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column, search_in_column
import re

class ValidadorDadosDosContratos:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['contratos'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'], max_files=keywords['max_files'])

    def predict_objeto(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['objeto_pattern'])
            result = search_in_column(self.df, self.keywords['objeto_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result

        result, isvalid = check_all_values_of_column(self.df, self.keywords['objeto'], typee='text')
        return isvalid, result

    def predict_valor(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['valor_pattern'])
            result = search_in_column(self.df, self.keywords['valor_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result
        
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor'], typee='valor')
        return isvalid, result
    
    def predict_favorecido(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['favorecido_pattern'])
            result = search_in_column(self.df, self.keywords['favorecido_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result
        
        result, isvalid = check_all_values_of_column(self.df, self.keywords['favorecido'], typee='text')
        return isvalid, result
    
    def predict_numero_ano_do_contrato(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['numero_ano_do_contrato_pattern'])
            result = search_in_column(self.df, self.keywords['numero_ano_do_contrato_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result

        result, isvalid = check_all_values_of_column(self.df, self.keywords['numero_ano_do_contrato'], typee='text')
        return isvalid, result
    
    def predict_vigencia(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['vigencia_pattern'])
            result = search_in_column(self.df, self.keywords['vigencia_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result

        result, isvalid = check_all_values_of_column(self.df, self.keywords['vigencia'], typee='text')
        return isvalid, result
    
    def predict_licitacao_de_origem(self):
        try:
            regex = self.keywords['regex']
        except KeyError:
            regex = False

        if regex is True:
            pattern = re.compile(self.keywords['licitacao_de_origem_pattern'])
            result = search_in_column(self.df, self.keywords['licitacao_de_origem_column'], pattern)
            isvalid = False
            if result['isvalid'].sum() > 0:
                isvalid = True
            return isvalid, result

        result, isvalid = check_all_values_of_column(self.df, self.keywords['licitacao_de_origem'], typee='text')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'objeto': {},
            'valor': {},
            'favorecido': {},
            'numero_ano_do_contrato': {},
            'vigencia': {},
            'licitacao_de_origem': {},
        }

        # Objeto
        isvalid, result = self.predict_objeto()
        result_explain = self.explain(result, 'objeto')
        resultados['objeto']['predict'] = isvalid
        resultados['objeto']['explain'] = result_explain

        # Valor
        isvalid, result = self.predict_valor()
        result_explain = self.explain(result, 'valor')
        resultados['valor']['predict'] = isvalid
        resultados['valor']['explain'] = result_explain

        # Favorecido
        isvalid, result = self.predict_favorecido()
        result_explain = self.explain(result, 'favorecido')
        resultados['favorecido']['predict'] = isvalid
        resultados['favorecido']['explain'] = result_explain

        # Número/Ano do contrato
        isvalid, result = self.predict_numero_ano_do_contrato()
        result_explain = self.explain(result, 'numero ou ano do contrato')
        resultados['numero_ano_do_contrato']['predict'] = isvalid
        resultados['numero_ano_do_contrato']['explain'] = result_explain

        # Vigência
        isvalid, result = self.predict_vigencia()
        result_explain = self.explain(result, 'vigência')
        resultados['vigencia']['predict'] = isvalid
        resultados['vigencia']['explain'] = result_explain

        # Licitação de origem
        isvalid, result = self.predict_licitacao_de_origem()
        result_explain = self.explain(result, 'licitação de origem')
        resultados['licitacao_de_origem']['predict'] = isvalid
        resultados['licitacao_de_origem']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade de entradas encontradas e analizadas que possuem o campo {description} do contrato válido: {sum(result['isvalid'])}"""
        return result