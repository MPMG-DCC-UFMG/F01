
from utils import indexing
from utils import check_df
from itertools import chain
from ..base import Validador
from utils import path_functions
from collections import defaultdict
from utils.search_html import analyze_html

# Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto	
class ValidadorGerarRelatorio(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords

        # Relatórios de contratos
        files_contratos = indexing.get_files(keywords['search_term_contratos'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search_contratos'])
        files_contratos = path_functions.filter_paths(files_contratos, words=['contratos'])
        files_contratos = path_functions.agg_paths_by_type(files_contratos)

        # Relatórios de licitações
        files_licitacoes = indexing.get_files(keywords['search_term_licitacoes'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search_licitacoes'])
        files_licitacoes = path_functions.filter_paths(files_licitacoes, words=['licitacao'])
        files_licitacoes = path_functions.agg_paths_by_type(files_licitacoes)

        files = defaultdict(list)
        for k, v in chain(files_contratos.items(), files_licitacoes.items()):
            files[k].extend(v)
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
            'gerar_relatorio': {},
        }

        isvalid, result = self.predict_relatorio(self.keywords['keyword_check'])
        result_explain = self.explain(result, self.keywords['keyword_check'])
        resultados_gerar_relatorio['gerar_relatorio']['predict'] = isvalid
        resultados_gerar_relatorio['gerar_relatorio']['explain'] = result_explain

        return resultados_gerar_relatorio


    def explain(self, result, keywords):

        if len(keywords) > 1:
            result = "Os palavras chaves {} estão presentes {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords, sum(result['matches']))
        else:
            result = "A palavra chave '{}' está presente {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords[0], sum(result['matches']))

        return result