from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

class ValidadorExecucao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        self.job_name = job_name

    def predict_item(self, item):
        keywords = self.keywords[item]
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['execucao'])
        files = path_functions.agg_paths_by_type(files)

        result = {"documentos":{}, "paginas":{}}

        result['documentos'] = len(files['pdf'])
        result_html = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        result['paginas'] = sum(result_html['matches'])
        isvalid = result['documentos'] > 0 or result['paginas'] > 0
        return isvalid, result   

    def explain(self, result, descricao):
        result = f"""Foram encontrados {result["documentos"]} pdfs na coleta que mencionam {descricao} e {result["paginas"]} menções em páginas html."""
        return result

    def predict(self):

        resultados = {
            'relatorios_quadrimestras_gestao_fiscal': {},
            'relatorio_bimestral_da_execucao_orcamentaria': {},
            'prestacao_anual_de_contas': {}
        }

        # Relatórios (quadrimestrais) de gestão fiscal e anexos
        isvalid, result = self.predict_item('relatorios_quadrimestras_gestao_fiscal')
        result_explain = self.explain(result, 'Relatórios (quadrimestrais) de gestão fiscal')
        resultados['relatorios_quadrimestras_gestao_fiscal']['predict'] = isvalid
        resultados['relatorios_quadrimestras_gestao_fiscal']['explain'] = result_explain

        # Relatórios (bimestrais) Resumido da Execução Orçamentária
        isvalid, result = self.predict_item('relatorio_bimestral_da_execucao_orcamentaria')
        result_explain = self.explain(result, 'Relatórios de Execução Orçamentária')
        resultados['relatorio_bimestral_da_execucao_orcamentaria']['predict'] = isvalid
        resultados['relatorio_bimestral_da_execucao_orcamentaria']['explain'] = result_explain

        # Prestação anual de contas, parecer prévio do TCE e julgamento pela Câmara de Vereadores
        isvalid, result = self.predict_item('prestacao_anual_de_contas')
        result_explain = self.explain(result, 'Prestação de contas')
        resultados['prestacao_anual_de_contas']['predict'] = isvalid
        resultados['prestacao_anual_de_contas']['explain'] = result_explain

        return resultados
