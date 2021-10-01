
import pandas as pd
import sys
import itertools
from datetime import date

sys.path.insert(0, '/home/cinthia/F01/src')

from utils import indexing
from utils import path_functions
from utils import search_html
from utils import read
from utils import check_df


def get_files_to_valid(
    search_term, index_keywords, num_matches,
    job_name, path_base, type='html', pattern='/tmp/es/data'): 
        
    #Search
    result = indexing.request_search(
      search_term=search_term, keywords=index_keywords, num_matches=num_matches, job_name=job_name)
      
    files = [i[2] for i in result]

    #Aggregate file by type
    agg_files = path_functions.agg_paths_bytype(files)

    #Return files in specific type
    html_files = agg_files.get(type)

    #Replace pattern by path_base
    if pattern != "":
        html_files = path_functions.create_valid_path (html_files, path_base=path_base, pattern=pattern)

    return html_files

def count_matches (text, keyword_to_search):

    matches = 0
    for i in keyword_to_search:
        matches += text.count(i)

    return matches

def analyze_html(html_files, keyword_to_search):

    matches = []

    for path in html_files:
        
        text = read.read_file(path)
        matches.append(count_matches (text, keyword_to_search))

    result = pd.DataFrame({'files': html_files, 'matches': matches})

    return result

def check_tags_address(soup, address):

    result = []
    for i in address:
        if(soup.find(id = i)) != None:
            result.append(soup.find(id = i).get_text())
        elif (soup.find(class_ = i)) != None:
            result.append(soup.find(class_ = i).get_text())

    result  = list(filter(None, result))

    return result

def analyze_tags(html_files):

    matches = []

    for path in html_files:
        
        soup = read.read_html(path)
        tags_id = search_html.get_tags_id (soup)
        tags_class = search_html.get_tags_class (soup)
        tags = list(itertools.chain(*[tags_id, tags_class]))
        tags_address = search_html.search_tags_address(tags)
        text = check_tags_address(soup, tags_address)

        matches.append(len(text))

    result = pd.DataFrame({'files': html_files, 'matches': matches, 'found_text': " ".join(text)})

    return result

def predict_search_engine (
    keyword_to_search, search_term, index_keywords, num_matches,
    job_name, path_base, pattern='/tmp/es/data', verbose=False):

    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, index_keywords, num_matches,
        job_name, path_base, pattern=pattern)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keyword_to_search)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Possui mecanismo de busca: {}".format(isvalid))

    return isvalid, result

def predict_update_infos(search_term, keywords, num_matches,
    job_name, path_base, pattern='/tmp/es/data', verbose=False):

    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, pattern=pattern)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Mantém as informações atualizadas: {}".format(isvalid))

    return isvalid, result

def predict_accessibility(search_term='acessibilidade', 
    keywords=['decreto nº 7.724', 'acessibilidade na divulgação das informações',
    'opção de contraste', 'trabalhar com leitores de páginas'], 
    num_matches=10, job_name="", path_base="", pattern='/tmp/es/data', verbose=False):
    
    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, pattern=pattern)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Possui intruções de acessibilidade: {}".format(isvalid))

    return isvalid, result

def predict_address(search_term="page-principal", 
    keywords=["portal", "informações", "servicos", "site", "municipal", "governo", "publico",
    "Prefeitura Municipal de Governador Valadares - Portal da Transparência", "Principal"],
    num_matches=10, job_name="", path_base="", pattern='/tmp/es/data', verbose=False):

    #Search
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, pattern=pattern)

    #Analyze all files
    result = analyze_tags(html_files)

    #Check all files
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Disponibiliza endereço e telefone de contato: {}".format(isvalid))

    return isvalid, result

def predict_export_reports(search_term='page-principal', 
    keywords=['pdf', 'xml', 'csv', 'xls', 'download', 'baixar', 'export', 'exportar'], 
    num_matches=10, job_name="", path_base="", pattern='/tmp/es/data', verbose=False):
    
    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, pattern=pattern)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Permite exportar relatórios: {}".format(isvalid))

    return isvalid, result

def explain(df, column_name, elemento):

    print("Explain - Quantidade de arquivos analizados: {}\n\tQuantidade de aquivos que possuem o item \"{}\" : {}\n".format(
         len(df[column_name]), sum(df[column_name]), elemento))

"""  
path_base = "/home/cinthia/F01/data"
pattern='/tmp/es/data'
num_matches = 10
job_name='index_governador_valadares'


todays_date = date.today()
search_term='RECEITAS - {}'.format(str(todays_date.year))
keywords=['RECEITAS - {}'.format(str(todays_date.year)), "DESPESAS - {}".format(str(todays_date.year)), str(todays_date.year)]

isvalid, result = predict_upadate_infos(
    search_term=search_term, keywords=keywords,
    num_matches=num_matches, job_name=job_name, path_base=path_base,
     pattern='/tmp/es/data', verbose=True)
explain(result, column_name='matches', elemento='Ferramenta de busca')

isvalid, result = predict_accessibility (
    num_matches=num_matches, job_name=job_name, path_base=path_base,
     pattern='/tmp/es/data', verbose=True)
explain(result, column_name='matches', elemento='Ferramenta de busca')

isvalid, result = predict_address(num_matches=10,
    job_name=job_name, path_base=path_base, verbose=True)
explain(result, column_name='matches', elemento='Disponibiliza Endereço')
"""
