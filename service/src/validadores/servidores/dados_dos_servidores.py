
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorDadosDosServidores:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        # print(self.df)

    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    def predict_cargo_funcao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo_funcao'], typee='text')
        return isvalid, result
    
    def predict_remuneracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao'], typee='text')
        return isvalid, result

    
    def predict(self):

        resultados = {
            'nome': {},
            'cargo_funcao': {},
            'remuneracao': {},
        }

        # # Nome
        # isvalid, result = self.predict_nome()
        # result_explain = self.explain(result, 'nome')
        # resultados['nome']['predict'] = isvalid
        # resultados['nome']['explain'] = result_explain

        # # Cargo/Função
        # isvalid, result = self.predict_cargo_funcao()
        # result_explain = self.explain(result, 'cargo / função')
        # resultados['cargo_funcao']['predict'] = isvalid
        # resultados['cargo_funcao']['explain'] = result_explain

        # # Remuneração
        # isvalid, result = self.predict_remuneracao()
        # result_explain = self.explain(result, 'remuneracao')
        # resultados['remuneracao']['predict'] = isvalid
        # resultados['remuneracao']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""Quantidade de entradas encontradas e analizadas que possuem o campo {description} do contrato válido: {sum(result['isvalid'])}"""
        return result