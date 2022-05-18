
# from codecs import ignore_errors
# import pandas as pd
# import sys
# import itertools
# from datetime import date
# import re
# import string

# sys.path.insert(0, '/home/cinthia/F01/src')

# from utils import indexing
# from utils.indexing import get_files_to_valid
# from utils import path_functions
# from utils import search_html
# from utils import read
# from utils import check_df

# def count_matches (text, keyword_to_search):

#     matches = 0
#     for i in keyword_to_search:
#         matches += text.lower().count(i.lower())

#     return matches

# def analyze_html(html_files, keyword_to_search):

#     matches = []
#     urls = []

#     for path in html_files:
        
#         text = read.read_file(path)
#         matches.append(count_matches (text, keyword_to_search))
#         urls.append(path_functions.get_url('/home/cinthia', path))

#     result = pd.DataFrame({'files': html_files, 'urls': urls, 'matches': matches})

#     return result

# def check_tags_address(soup, address):

#     result = []
#     for i in address:
#         if(soup.find(id = i)) != None:
#             result.append(soup.find(id = i).get_text())
#         elif (soup.find(class_ = i)) != None:
#             result.append(soup.find(class_ = i).get_text())

#     result  = list(filter(None, result))

#     return result

# def analyze_tags(html_files):

#     matches = []
#     urls = []
#     found_text = []

#     for path in html_files:
        
#         soup = read.read_html(path)
#         tags_id = search_html.get_tags_id (soup)
#         tags_class = search_html.get_tags_class (soup)
#         tags = list(itertools.chain(*[tags_id, tags_class]))
#         tags_address = search_html.search_tags_address(tags)
#         text = check_tags_address(soup, tags_address)

#         text = str(' '.join(text).encode('ascii','ignore'))

#         x = re.search(r"(rua|Rua|Av|Avenida|Praça)(.*)\s([\s\w]*),\s\b[0-9]{1,6}\s*([\-]|[\|]|[  +]|[\,])?\s([\s\w]*)", text, re.IGNORECASE)
#         if x == None:
#             matches.append(0)
#             found_text.append('')
#         else:
#             matches.append(1)
#             found_text.append(x.group())

#         urls.append(path_functions.get_url('/home/cinthia', path))

#     try:
#         result = pd.DataFrame({'files': html_files, 'matches': matches, 'urls':urls, 'found_text': found_text})
#     except UnboundLocalError:
#         result = pd.DataFrame({'files': [], 'matches': [], 'urls': [], 'found_text': ""})

#     result.to_csv("test.csv")
#     return result


# def explain(df, column_name, elemento, verbose=False):
    
#     match_url = list(df.loc[df['matches'] > 0]['urls'])

#     result = {'num_analisados': len(df[column_name]),
#               'num_matches': sum(df[column_name]),
#               'match_link': match_url,
#               'item': elemento}

#     if verbose:
#         print(result)

#     return result


from utils import indexing
from utils import check_df
from ..base import Validador
from utils import path_functions
from utils.search_html import analyze_html

class ValidadorRequisitosExigidos(Validador):

    def __init__(self, job_name, keywords):
        self.job_name = job_name
        self.keywords = keywords

    # Contém ferramenta de pesquisa de conteúdo que permite o acesso à informação 
        # (a ferramenta “lupa” para promover pesquisas no próprio sítio eletrônico)	
    def predict_busca(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_exportar_relatorios(self, keywords):
        
        #Search all files
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)
        
        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_info_atualizadas(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result
    
    def predict_contato(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['requisitos_exigidos'])
        files = path_functions.agg_paths_by_type(files)

        #Analyze all html files searching keywords
        result = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        #Check result 
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict_acessibilidade(self, keywords):

        #Search all files
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], self.job_name, keywords_search=keywords['keywords_to_search'])
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
