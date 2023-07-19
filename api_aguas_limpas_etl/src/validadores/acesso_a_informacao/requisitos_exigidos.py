from src.validadores.utils import indexing
from src.validadores.utils import check_df
from ..base import Validador
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

class ValidadorRequisitosExigidos(Validador):

    def __init__(self, job_name, keywords):
        self.job_name = job_name
        self.keywords = keywords

    # Contém ferramenta de pesquisa de conteúdo que permite o acesso à informação 
        # (a ferramenta “lupa” para promover pesquisas no próprio sítio eletrônico)	
    def predict_busca(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_exportar_relatorios(self, keywords):
        
        #Search all files
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)
        
        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_info_atualizadas(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result
    
    def predict_contato(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_acessibilidade(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict(self):

        resultados_requisitos_exigidos = {
            'busca': {},
            'exportar_relatorios': {},
            'info_atualizadas': {},
            'contato': {},
            'acessibilidade': {},
        }

        # Busca
        isvalid, result = self.predict_busca(self.keywords['busca'])
        result_explain = self.explain(result)
        resultados_requisitos_exigidos['busca']['predict'] = isvalid
        resultados_requisitos_exigidos['busca']['explain'] = result_explain

        # Exportar Relatorios
        isvalid, result = self.predict_exportar_relatorios(self.keywords['exportar_relatorios'])
        result_explain = self.explain(result)
        resultados_requisitos_exigidos['exportar_relatorios']['predict'] = isvalid
        resultados_requisitos_exigidos['exportar_relatorios']['explain'] = result_explain

        # Informaçẽos atualizadas
        isvalid, result = self.predict_info_atualizadas(self.keywords['info_atualizadas'])
        result_explain = self.explain(result)
        resultados_requisitos_exigidos['info_atualizadas']['predict'] = isvalid
        resultados_requisitos_exigidos['info_atualizadas']['explain'] = result_explain

        isvalid, result = self.predict_contato(self.keywords['contato'])
        result_explain = self.explain(result)
        resultados_requisitos_exigidos['contato']['predict'] = isvalid
        resultados_requisitos_exigidos['contato']['explain'] = result_explain

        isvalid, result = self.predict_acessibilidade(self.keywords['acessibilidade'])
        result_explain = self.explain(result)
        resultados_requisitos_exigidos['acessibilidade']['predict'] = isvalid
        resultados_requisitos_exigidos['acessibilidade']['explain'] = result_explain

        return resultados_requisitos_exigidos

    def explain(self, result):
        result = result.query('matches > 0')
        result_explain = ""
        for index, row in result.iterrows():
            result_explain += f"No arquivo \'{row[0]}\' foi encontrado {row[2]}. "

        return result_explain
