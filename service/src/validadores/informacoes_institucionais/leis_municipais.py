import numpy as np
from ..base import Validador
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import checker
from src.validadores.utils.check_df import contains_keyword
from src.validadores.utils.file_to_dataframe import get_df

class ValidadorLeisMunicipais(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        self.job_name = job_name
        if self.keywords['type'] != 'predict_by_number_of_files':
            files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
            files = path_functions.filter_paths(files, words=['informacoes_institucionais'])
            self.files = path_functions.agg_paths_by_type(files)
            self.df = get_df(self.files, keywords['types'])

    def predict_leis_municipais(self):
        result = {
            'leis':0,
            'decretos': 0,
            'portarias': 0,
            'resolucoes': 0
        }

        df = self.df.copy()

        contem, keyword = contains_keyword(df, self.keywords['leis_municipais'])
        if (not contem):
            return False, result

        vfunc = np.vectorize(checker.check_keyword)
        df['leis_'] =  vfunc(df[keyword], "lei" )
        result['leis'] = df['leis_'].sum()

        vfunc = np.vectorize(checker.check_keyword)
        df['decretos_'] =  vfunc(df[keyword],"decretos")
        result['decretos'] = df['decretos_'].sum()

        vfunc = np.vectorize(checker.check_keyword)
        df['portarias_'] =  vfunc(df[keyword],"portarias")
        result['portarias'] = df['portarias_'].sum()

        vfunc = np.vectorize(checker.check_keyword)
        df['resolucoes_'] =  vfunc(df[keyword],"resoluções")
        result['resolucoes'] = df['resolucoes_'].sum()

        # Caso existam leis, decretos, portarias ou resolucoes retorna TRUE
        return (any([item[1] for item in result.items()])), result
    
    def explain_leis_municipais(self, result):
        result = f"""Quantidade de entradas de leis encontradas: {result['leis']}.
        Quantidade de entradas de decretos encontradas: {result['decretos']}.
        Quantidade de entradas de portarias encontradas: {result['portarias']}.
        Quantidade de entradas de resoluções encontradas: {result['resolucoes']}.
        """
        return result

    def predict(self):

        resultados = {
            'leis_municipais': {},
        }

        # Link de acesso legislação

        if self.keywords['type'] == 'predict_by_number_of_files':
            # Prever pela quantida de arquivos
            isvalid, result = self.predict_by_number_of_files(self.job_name, self.keywords['directory'])
            result_explain = self.explain_by_number_of_files(isvalid, result)

        else:
            # Prever pelo conteudo encontrado
            isvalid, result = self.predict_leis_municipais()
            result_explain = self.explain_leis_municipais(result)
        
        resultados['leis_municipais']['predict'] = isvalid
        resultados['leis_municipais']['explain'] = result_explain

        return resultados

    def explain(self, result, description):
        try:
            numero_de_entradas = len(result)
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} válido: {sum(result['isvalid'])}"""
        return "result"