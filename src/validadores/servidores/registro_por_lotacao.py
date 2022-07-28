
from utils import indexing
from utils import path_functions
from utils.file_to_df import get_df
from utils.check_df import check_all_values_of_column
from utils.check_df import search_in_column

class ValidadorRegistroPorLotacao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_matricula(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['matricula'], typee='text')
        return isvalid, result

    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    def predict_cargo_funcao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo_funcao'], typee='text')
        return isvalid, result
    
    def predict_remuneracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao'], typee='text')
        return isvalid, result
    
    def predict_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['abate_teto'], typee='text')
        return isvalid, result

    def predict_tipo_de_vinculo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['tipo_de_vinculo'], typee='text')
        return isvalid, result

    
    def predict(self):

        resultados = {
            'matricula': {'predict': False, 'explain': 'Não possui lotação'},
            'nome': {'predict': False, 'explain': 'Não possui lotação'},
            'cargo_funcao': {'predict': False, 'explain': 'Não possui lotação'},
            'remuneracao': {'predict': False, 'explain': 'Não possui lotação'},
            'abate_teto': {'predict': False, 'explain': 'Não possui lotação'},
            'tipo_de_vinculo': {'predict': False, 'explain': 'Não possui lotação'},
        }

        # - validar se existe uma coluna "lotação"

        _, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')

        if isvalid:
        # - validar os itens

            # Matrícula
            isvalid, result = self.predict_matricula()
            result_explain = self.explain(result, 'matrícula')
            resultados['matricula']['predict'] = isvalid
            resultados['matricula']['explain'] = result_explain

            # Nome
            isvalid, result = self.predict_nome()
            result_explain = self.explain(result, 'nome')
            resultados['nome']['predict'] = isvalid
            resultados['nome']['explain'] = result_explain

            # Cargo/Função
            isvalid, result = self.predict_cargo_funcao()
            result_explain = self.explain(result, 'cargo/função')
            resultados['cargo_funcao']['predict'] = isvalid
            resultados['cargo_funcao']['explain'] = result_explain

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