from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column, search_in_column

class ValidadorDadosParaAcompanhamento:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        print(len(files))
        files = path_functions.filter_paths(files, words=['obras_publicas'])
        print(len(files))
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_objeto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['objeto'], typee='text')
        return isvalid, result

    def predict_valor_total(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor_total'], typee='text')
        return isvalid, result
    
    def predict_empresa_contratada(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['empresa_contratada'], typee='text')
        return isvalid, result
    
    def predict_data_de_inicio(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data_de_inicio'], typee='text')
        return isvalid, result
    
    def predict_data_prevista_ou_prazo_de_execucao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['data_prevista_ou_prazo_de_execucao'], typee='text')
        return isvalid, result
    
    def predict_valor_total_pago_ou_percentual(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valor_total_pago_ou_percentual'], typee='text')
        return isvalid, result

    def predict_situacao_atual(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['situacao_atual'], typee='text')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'objeto': {},
            'valor_total': {},
            'empresa_contratada': {},
            'data_de_inicio': {},
            'data_prevista_ou_prazo_de_execucao': {},
            'valor_total_pago_ou_percentual': {},
            'situacao_atual': {},
        }

        # Objeto
        isvalid, result = self.predict_objeto()
        result_explain = self.explain(result, f"\"{self.keywords['objeto']}\"")
        resultados['objeto']['predict'] = isvalid
        resultados['objeto']['explain'] = result_explain

        # Valor total
        isvalid, result = self.predict_valor_total()
        result_explain = self.explain(result, f"\"{self.keywords['valor_total']}\"")
        resultados['valor_total']['predict'] = isvalid
        resultados['valor_total']['explain'] = result_explain

        # Empresa contratada
        isvalid, result = self.predict_empresa_contratada()
        result_explain = self.explain(result, f"\"{self.keywords['empresa_contratada']}\"")
        resultados['empresa_contratada']['predict'] = isvalid
        resultados['empresa_contratada']['explain'] = result_explain

        # Data de início
        isvalid, result = self.predict_data_de_inicio()
        result_explain = self.explain(result, f"\"{self.keywords['data_de_inicio']}\"")
        resultados['data_de_inicio']['predict'] = isvalid
        resultados['data_de_inicio']['explain'] = result_explain

        # Data prevista para término ou prazo de execução
        isvalid, result = self.predict_data_prevista_ou_prazo_de_execucao()
        result_explain = self.explain(result, f"\"{self.keywords['data_prevista_ou_prazo_de_execucao']}\"")
        resultados['data_prevista_ou_prazo_de_execucao']['predict'] = isvalid
        resultados['data_prevista_ou_prazo_de_execucao']['explain'] = result_explain

        # Valor total já pago ou percentual de execução financeira
        isvalid, result = self.predict_valor_total_pago_ou_percentual()
        result_explain = self.explain(result, f"\"{self.keywords['valor_total_pago_ou_percentual']}\"")
        resultados['valor_total_pago_ou_percentual']['predict'] = isvalid
        resultados['valor_total_pago_ou_percentual']['explain'] = result_explain

        # Situação atual da obra
        isvalid, result = self.predict_situacao_atual()
        result_explain = self.explain(result, f"\"{self.keywords['situacao_atual']}\"")
        resultados['situacao_atual']['predict'] = isvalid
        resultados['situacao_atual']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade de entradas encontradas e analizadas que possuem {description}: {sum(result['isvalid'])}"""
        return result