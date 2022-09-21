
from src.validadores.utils import indexing
from src.validadores.utils import check_df
from ..base import Validador
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

# Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto	
class ValidadorConteudoIntegral(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['contratos'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files

    def predict_relatorio(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict(self):

        resultados_gerar_relatorio = {
            'conteudo_integral': {},
        }

        isvalid, result = self.predict_relatorio(self.keywords['keyword_check'])
        result_explain = self.explain(result, self.keywords['keyword_check'])
        resultados_gerar_relatorio['conteudo_integral']['predict'] = isvalid
        resultados_gerar_relatorio['conteudo_integral']['explain'] = result_explain

        return resultados_gerar_relatorio


    def explain(self, result, keywords):

        if len(keywords) > 1:
            result = "Os palavras chaves {} estão presentes {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords, sum(result['matches']))
        else:
            result = "A palavra chave '{}' está presente {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords[0], sum(result['matches']))

        return result