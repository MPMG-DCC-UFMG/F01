import numpy as np
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import checker
from src.validadores.utils.check_df import contains_keyword
from src.validadores.utils.file_to_dataframe import get_df

class ValidadorLinkDeAcesso:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['informacoes_institucionais'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_link_de_acesso(self):
        result = {
            'leis':0,
            'decretos': 0,
            'portarias': 0,
            'resolucoes': 0
        }

        df = self.df.copy()

        contem, keyword = contains_keyword(df, self.keywords['link_de_acesso'])
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
    
    def explain_link_de_acesso(self, result):
        result = f"""Quantidade de entradas de leis encontradas: {result['leis']}.
        Quantidade de entradas de decretos encontradas: {result['decretos']}.
        Quantidade de entradas de portarias encontradas: {result['portarias']}.
        Quantidade de entradas de resoluções encontradas: {result['resolucoes']}.
        """
        return result

    def predict(self):

        resultados = {
            'link_de_acesso': {},
        }

        # Link de acesso legislação
        isvalid, result = self.predict_link_de_acesso()
        result_explain = self.explain_link_de_acesso(result)
        resultados['link_de_acesso']['predict'] = isvalid
        resultados['link_de_acesso']['explain'] = result_explain

        return resultados

    def explain(self, result, description):
        try:
            numero_de_entradas = len(result)
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} válido: {sum(result['isvalid'])}"""
        return "result"