from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.check_df import infos_isvalid
from src.validadores.utils.search_html import analyze_html

class ValidadorResultadosDasLicitacoes:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['licitacao'])
        self.files = path_functions.agg_paths_by_type(files)

    def predict_resultado_das_licitacoes(self):

        files = self.files['html']

        result = analyze_html(files, keyword_to_search=self.keywords['resultados'])
        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result
    
    def predict(self):

        resultados = {
            'resultados_das_licitacoes': {}
        }

        # Resultados das licitacoes
        isvalid, result = self.predict_resultado_das_licitacoes()
        result_explain = self.explain(result)
        resultados['resultados_das_licitacoes']['predict'] = isvalid
        resultados['resultados_das_licitacoes']['explain'] = result_explain

        return resultados

    def explain(self, result):
        result = result.query('matches > 0')
        result_explain = ""
        for index, row in result.iterrows():
            result_explain += f"No arquivo \'{row[0]}\' foi encontrado {row[2]}. "

        return result_explain