
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.check_df import search_in_column

class ValidadorRegistroDaRemuneracao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        # print(self.df)

    def predict_agentes_politicos(self):
        keywords = ["prefeito", "secretário municipal"]
        result = search_in_column(self.df, self.keywords['agentes_politicos'], keywords)

        isvalid = any(result['isvalid'])
        return isvalid, result

    def predict_contratados_temporariamente(self):
        keywords = ["temporário", "temporariamente"]
        result = search_in_column(self.df, self.keywords['contratados_temporariamente'], keywords)

        isvalid = any(result['isvalid'])
        return isvalid, result
    
    def predict_servidores_efetivos_ou_empregados_publicos(self):
        keywords = ["efetivo", "empregado público"]
        result = search_in_column(self.df, self.keywords['servidores_efetivos_ou_empregados_publicos'], keywords)

        isvalid = any(result['isvalid'])
        return isvalid, result

    
    def predict(self):

        resultados = {
            'agentes_politicos': {},
            'contratados_temporariamente': {},
            'servidores_efetivos_ou_empregados_publicos': {},
        }

        # Agentes políticos
        isvalid, result = self.predict_agentes_politicos()
        result_explain = self.explain(result, 'agentes políticos')
        resultados['agentes_politicos']['predict'] = isvalid
        resultados['agentes_politicos']['explain'] = result_explain

        # # Contratados temporariamente
        isvalid, result = self.predict_contratados_temporariamente()
        result_explain = self.explain(result, 'contratados temporariamente')
        resultados['contratados_temporariamente']['predict'] = isvalid
        resultados['contratados_temporariamente']['explain'] = result_explain

        # # Servidores efetivos ou empregados públicos
        isvalid, result = self.predict_servidores_efetivos_ou_empregados_publicos()
        result_explain = self.explain(result, 'servidores efetivos ou empregados publicos')
        resultados['servidores_efetivos_ou_empregados_publicos']['predict'] = isvalid
        resultados['servidores_efetivos_ou_empregados_publicos']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        try:
            result = f"""Quantidade de registros de {description} encontrados: {sum(result['isvalid'])}"""
            return result
        except KeyError:
            return "Não encontrado"