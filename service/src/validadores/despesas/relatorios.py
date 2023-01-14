from src.validadores.utils import indexing
from src.validadores.utils import check_df
from ..base import Validador
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_columns

class ValidadorRelatorios(Validador):

    def __init__(self, job_name, keywords):
        self.job_name = job_name
        self.keywords = keywords

    # Link de acesso ao Plano Plurianual do município
    def predict_plano_plurianual(self,keywords):
        
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=keywords['filter_paths'])
        files = path_functions.agg_paths_by_type(files)

        if (keywords['tipo_do_validador'] == 'get_df'):
            df = get_df(files, keywords['types'])
            print(keywords['valores_esperados'])
            check_columns(df, keywords['valores_esperados'])

        # if (keywords['tipo_do_validador'] == 'line_search'):
            # result = line_search(files)

        else:
            result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        # #Check result 
        # threshold = keywords['threshold_type']
        # if (keywords['threshold_type'] == "file"):
        #     threshold = keywords['threshold'] * len(files)
        # isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=threshold)
        # return isvalid, result
        return False, []

    def explain_plano_plurianual(self, result, keywords):

        result_explain = (
            "Opção de visualizar ou baixar Plano Plurianual do município foi encontrado em {} arquivos".format(
                (len(result.query(f"matches > {keywords['threshold']}"))))
        )
        return result_explain

    # Link de acesso à Lei de Diretrizes Orçamentarias do município
    def predict_lei_diretrizes_orcamentarias(self,keywords):
        
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['leis_orcamentarias'])
        files = path_functions.agg_paths_by_type(files)
        files = files['html']

        # Analyze 
        result = analyze_html(files, keyword_to_search=keywords['keyword_check'])
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)
        return isvalid, result

    def explain_lei_diretrizes_orcamentarias(self, result):

        result_explain = ("Opção de visualizar ou baixar a Lei de Diretrizes Orçamentarias foi encontrado em {} arquivos".format((len(result.query('matches > 1')))))
        return result_explain

    # Link de acesso à Lei Orçamentária Anual do município
    def predict_lei_orcamentaria_anual(self,keywords):
        
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['leis_orcamentarias'])
        files = path_functions.agg_paths_by_type(files)
        files = files['html']
        print(files)

        # Analyze 
        result = analyze_html(files, keyword_to_search=keywords['keyword_check'])
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)
        print(result)
        return isvalid, result

    def explain_lei_orcamentaria_anual(self, result):

        result_explain = ("Opção de visualizar ou baixar a Lei de Orcamentaria Anul foi encontrado em {} arquivos".format((len(result.query('matches > 1')))))
        return result_explain


    # Apresentação do balanço anual, com as respectivas demonstrações contábeis
    def predict_balanco_demonstracoes(self,keywords):

        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['leis_orcamentarias'])
        files = path_functions.agg_paths_by_type(files)
        files = files['html']

        # Analyze 
        result = analyze_html(files, keyword_to_search=keywords['keyword_check'])
        
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    # Relatórios da execução orçamentária e gestão fiscal
    def predict_execucao_orcamentaria_gestao_fiscal(self,keywords):

        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['leis_orcamentarias'])
        files = path_functions.agg_paths_by_type(files)
        files = files['html']

        # Analyze 
        result = analyze_html(files, keyword_to_search=keywords['keyword_check'])
        
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict(self):
        resultados_relatorios = {
              'plano_plurianual': {},
              'lei_diretrizes_orcamentarias': {},
              'lei_orcamentaria_anual': {},
              'balanco_demonstracoes': {},
              'execucao_orcamentaria_gestao_fiscal': {}
              }

        isvalid, result = self.predict_plano_plurianual(keywords=self.keywords['plano_plurianual'])
        # result_explain = self.explain_plano_plurianual(result, self.keywords['plano_plurianual'])
        resultados_relatorios['plano_plurianual']['predict'] = isvalid
        # resultados_relatorios['plano_plurianual']['explain'] = result_explain

        # isvalid, result = self.predict_lei_diretrizes_orcamentarias(keywords=self.keywords['lei_diretrizes_orcamentarias'])
        # result_explain = self.explain_lei_diretrizes_orcamentarias(result)
        # resultados_relatorios['lei_diretrizes_orcamentarias']['predict'] = isvalid
        # resultados_relatorios['lei_diretrizes_orcamentarias']['explain'] = result_explain

        # isvalid, result = self.predict_lei_orcamentaria_anual(keywords=self.keywords['lei_orcamentaria_anual'])
        # result_explain = self.explain_lei_orcamentaria_anual(result)
        # resultados_relatorios['lei_orcamentaria_anual']['predict'] = isvalid
        # resultados_relatorios['lei_orcamentaria_anual']['explain'] = result_explain

        # isvalid, result = self.predict_balanco_demonstracoes(keywords=self.keywords['balanco_demonstracoes'])
        # result_explain = self.explain_balanco_demonstracoes()
        # resultados_relatorios['balanco_demonstracoes']['predict'] = isvalid
        # resultados_relatorios['balanco_demonstracoes']['explain'] = result_explain

        # isvalid, result = self.predict_execucao_orcamentaria_gestao_fiscal(keywords=self.keywords['execucao_orcamentaria_gestao_fiscal'])
        # result_explain = self.explain()
        # resultados_relatorios['gerar_relatorios']['predict'] = isvalid
        # resultados_relatorios['gerar_relatorios']['explain'] = result_explain

        return resultados_relatorios

    def explain(self, result):

        return result

