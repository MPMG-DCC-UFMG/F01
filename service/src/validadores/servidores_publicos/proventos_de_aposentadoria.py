
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.check_df import search_in_column

class ValidadorProventosDeAposentadoria:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    def predict_cargo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo'], typee='text')
        return isvalid, result
    
    def predict_remuneracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao'], typee='text')
        return isvalid, result
    
    def predict_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['abate_teto'], typee='text')
        return isvalid, result

    def predict_remuneracao_retirando_o_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['tipo_de_vinculo'], typee='text')
        return isvalid, result
    
    def predict_tipo_de_vinculo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['tipo_de_vinculo'], typee='text')
        return isvalid, result

    def predict(self):

        resultados = {
            'nome': {'predict': False, 'explain': 'Não possui lotação'},
            'cargo': {'predict': False, 'explain': 'Não possui lotação'},
            'remuneracao': {'predict': False, 'explain': 'Não possui lotação'},
            'abate_teto': {'predict': False, 'explain': 'Não possui lotação'},
            'remuneracao_retirando_o_abate_teto': {'predict': False, 'explain': 'Não possui lotação'},
            'tipo_de_vinculo': {'predict': False, 'explain': 'Não possui lotação'},
        }

        # - Filtar os que são aposentados
        try:
            column_to_filter = self.keywords['aposentadoria']
            self.df = self.df[self.df[column_to_filter].str.contains('aposent', regex= True, na=False, case=False)]
        except KeyError:
            return resultados

        # - validar os itens

        # Nome
        isvalid, result = self.predict_nome()
        result_explain = self.explain(result, 'nome')
        resultados['nome']['predict'] = isvalid
        resultados['nome']['explain'] = result_explain

        # Cargo
        isvalid, result = self.predict_cargo()
        result_explain = self.explain(result, 'cargo')
        resultados['cargo']['predict'] = isvalid
        resultados['cargo']['explain'] = result_explain

        # Remuneração
        isvalid, result = self.predict_remuneracao()
        result_explain = self.explain(result, 'remuneração')
        resultados['remuneracao']['predict'] = isvalid
        resultados['remuneracao']['explain'] = result_explain

        # Abate teto
        isvalid, result = self.predict_abate_teto()
        result_explain = self.explain(result, 'abate teto')
        resultados['abate_teto']['predict'] = isvalid
        resultados['abate_teto']['explain'] = result_explain

        # Remuneração retirando o abate teto
        isvalid, result = self.predict_remuneracao_retirando_o_abate_teto()
        result_explain = self.explain(result, 'remuneração retirando o abate teto')
        resultados['remuneracao_retirando_o_abate_teto']['predict'] = isvalid
        resultados['remuneracao_retirando_o_abate_teto']['explain'] = result_explain

        # Tipo de vínculo
        isvalid, result = self.predict_tipo_de_vinculo()
        result_explain = self.explain(result, 'tipo de vínculo')
        resultados['tipo_de_vinculo']['predict'] = isvalid
        resultados['tipo_de_vinculo']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        try:
            result = f"""Quantidade de registros de {description} encontrados: {sum(result['isvalid'])}"""
            return result
        except KeyError:
            return "Não encontrado"