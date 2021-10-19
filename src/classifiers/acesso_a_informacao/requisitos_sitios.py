
from codecs import ignore_errors
import pandas as pd
import sys
import itertools
from datetime import date
import re
import string

sys.path.insert(0, '/home/cinthia/F01/src')

from utils import indexing
from utils import path_functions
from utils import search_html
from utils import read
from utils import check_df


def get_files_to_valid(
    search_term, index_keywords, num_matches,
    job_name, path_base, type='html'): 
        
    #Search
    result = indexing.request_search(
      search_term=search_term, keywords=index_keywords, num_matches=num_matches, job_name=job_name)
      
    files = [i[2] for i in result]

    #Aggregate file by type
    agg_files = path_functions.agg_paths_by_type(files)

    #Return files in specific type
    html_files = agg_files.get(type)

    return html_files

def count_matches (text, keyword_to_search):

    matches = 0
    for i in keyword_to_search:
        matches += text.count(i)

    return matches

def analyze_html(html_files, keyword_to_search):

    matches = []
    urls = []

    for path in html_files:
        
        text = read.read_file(path)
        matches.append(count_matches (text, keyword_to_search))
        urls.append(path_functions.get_url('/home/cinthia', path))

    result = pd.DataFrame({'files': html_files, 'urls': urls, 'matches': matches})

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
    urls = []
    found_text = []

    for path in html_files:
        
        soup = read.read_html(path)
        tags_id = search_html.get_tags_id (soup)
        tags_class = search_html.get_tags_class (soup)
        tags = list(itertools.chain(*[tags_id, tags_class]))
        tags_address = search_html.search_tags_address(tags)
        text = check_tags_address(soup, tags_address)

        text = str(' '.join(text).encode('ascii','ignore'))

        x = re.search(r"(rua|Rua|Av|Avenida|Praça)(.*)\s([\s\w]*),\s\b[0-9]{1,6}\s*([\-]|[\|]|[  +]|[\,])?\s([\s\w]*)", text, re.IGNORECASE)
        if x == None:
            matches.append(0)
            found_text.append('')
        else:
            matches.append(1)
            found_text.append(x.group())

        urls.append(path_functions.get_url('/home/cinthia', path))

    try:
        result = pd.DataFrame({'files': html_files, 'matches': matches, 'urls':urls, 'found_text': found_text})
    except UnboundLocalError:
        result = pd.DataFrame({'files': [], 'matches': [], 'urls': [], 'found_text': ""})

    result.to_csv("test.csv")
    return result

def predict_search_engine (
    search_term='busca', keywords="", num_matches=10,
    job_name="", path_base="", verbose=False):

    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Possui mecanismo de busca: {}".format(isvalid))

    return isvalid, result

def predict_update_infos(
    search_term, keywords=["", 'baixar'], num_matches=10, job_name="",
     path_base="", verbose=False):

    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

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
    num_matches=10, job_name="", path_base="", verbose=False):
    
    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

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
    num_matches=10, job_name="", path_base="", verbose=False):

    #Search
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    #Analyze all files
    result = analyze_tags(html_files)

    #Check all files
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Disponibiliza endereço e telefone de contato: {}".format(isvalid))

    return isvalid, result

def predict_export_reports(search_term='page-principal', 
    keywords=['pdf', 'xml', 'csv', 'xls', 'download', 'baixar', 'export', 'exportar'], 
    num_matches=10, job_name="", path_base="", verbose=False):
    
    #Search all files using keywords
    html_files = get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base,)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Permite exportar relatórios: {}".format(isvalid))

    return isvalid, result

def explain(df, column_name, elemento, verbose=False):
    
    match_url = list(df.loc[df['matches'] > 0]['urls'])

    result = {'num_analisados': len(df[column_name]),
              'num_matches': sum(df[column_name]),
              'match_link': match_url,
              'item': elemento}

    if verbose:
        print(result)

    return result

