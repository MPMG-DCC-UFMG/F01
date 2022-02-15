from bs4 import BeautifulSoup
from click import types
import pandas as pd
import re
import os
import sys
from itertools import chain
from collections import defaultdict
#sys.path.insert(0, '/home/cinthia/F01/src')

from pathlib import Path

from pandas.io import html

sys.path.insert(0, '../')

from utils import indexing
from utils import html_to_csv
from utils import path_functions
from utils import check_df

def analyze_proc_lici(df, keywords): 
    """
    Verifica se existem colunas para cada palavra-chave e a quantidade de valores nulos
    em cada uma delas
    """

    val = { i: [] for i in keywords}

    for i in keywords:

        isvalid, column_name = check_df.contains_keyword(df=df, word=i)
        # print(isvalid, '|', column_name,'|' ,i)

        if isvalid:
            val[i] = list(~df[column_name].isna())
        else:
            val[i] = []
    
    return val

def analyze_inexibilidade (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é inexibilidade
    """

    try:
        if re.search("inexigibilidade", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False

    except TypeError:
        return False

def analyze_dispensa (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é dispensa
    """

    try:
        if re.search("dispensa", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False

    except TypeError:
        return False

def analyze_resultado (df, column_name):
    """
    Verifica se na coluna resultado há algum arquivo
    """
    if len(df[column_name].value_counts()) > 1:
        return True
    else:
        return False

def analyze_busca(format_path):
    """
    Verifica se os documentos html possuem o campo "Filtrar Pesquisa"
    """

    try:
        soup = BeautifulSoup(open(format_path), features="lxml")
        text = soup.get_text()

        if re.search("filtrar\s*pesquisa|filtrar", text, re.IGNORECASE) != None:
            return True
    
    except TypeError and UnicodeDecodeError:
        return False
    except UnicodeDecodeError:    
        return False
        
    return False

def analyze_edital(df, column_name):
    """
    Verifica se na coluna Editais há algum arquivo
    """
    if len(df[column_name].value_counts()) > 1:
        return True
    else:
        return False

def check_all_files_busca(paths, result):

    for file_name in paths:
        print(file_name)
        result['busca'].append(analyze_busca(file_name))

    return result


def predict_proc_lic(
    search_term, keywords_search, path_base, num_matches=100,
    keywords_check=['número', 'modalidade', 'objeto', 'status', 'editais'],
    filter_word='licitacao', job_name='index', threshold = 0, pattern='/tmp/es/data', types='html'): 

    result_html = {'proc_lic': {}}
    result_bat = {'proc_lic': {}}
    result_pdf = {'proc_lic': {}}

    #Search
    files = indexing.get_files(
        search_term, keywords_search, num_matches,
        job_name, path_base)

    files = path_functions.filter_paths(files, filter_word)
        
    files = path_functions.agg_paths_by_type2(files)

    for key, values in files.items():
        
        if key == 'html' and 'html' in types:
            #Convert
            df_html = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            result_html['proc_lic'] = analyze_proc_lici(df_html, keywords_check)

        if key == 'bat' and 'bat' in types:
            #Convert
            df_bat = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            #Analyze
            result_bat['proc_lic'] = analyze_proc_lici(df_bat, keywords_check)

        if key == 'pdf' and 'pdf' in types:
            #Convert
            df_pdfs = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df_pdfs = df_pdfs.drop_duplicates()
            #Analyze
            result_pdf['proc_lic'] = analyze_proc_lici(df_pdfs, keywords_check)

    result = defaultdict(list)
    for k, v in chain(result_html['proc_lic'].items(), result_bat['proc_lic'].items(), result_pdf['proc_lic'].items()):
        result[k].extend(v)

    result = {'proc_lic': dict(result)}

    #Check
    isvalid = []
    for i in keywords_check:
        isvalid.append(check_df.infos_isvalid(result['proc_lic'], i, threshold=threshold))

    return isvalid, result


def predict_inexigibilidade(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitac', job_name='index', threshold=0, pattern='/tmp/es/data', types='html'): 

    result = {'inexigibilidade': []}
    df = pd.DataFrame()

    #Search
    files = indexing.get_files(
        search_term, keywords_search, num_matches,
        job_name, path_base)

    files = path_functions.filter_paths(files, filter_word)
        
    files = path_functions.agg_paths_by_type2(files)

    for key, values in files.items():
        
        if key == 'html' and 'html' in types:
            #Convert
            df_html = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df = pd.concat([df, df_html])

        if key == 'bat' and 'bat' in types:
            #Convert
            df_bat = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df = pd.concat([df, df_bat])

        if key == 'pdf' and 'pdf' in types:
            #Convert
            df_pdfs = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df_pdfs = df_pdfs.drop_duplicates()
            df = pd.concat([df, df_pdfs])
            #Analyze


    if "Número Modalidade" in df.columns:
        df.drop(columns=["Número Modalidade"],inplace=True)

    #Analyze
    isvalid, column_modalidade = check_df.contains_keyword(df, word='modalidade')

    print('column_modalidade',column_modalidade)

    for index, value in df.iterrows():
        result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))
            
    print(result)
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='inexigibilidade', threshold=threshold)
        
    return isvalid, result

def predict_dispensa(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitac', job_name='index', threshold=0, pattern='/tmp/es/data', types='html'): 

    result = {'dispensa': []}
    df = pd.DataFrame()

    #Search
    files = indexing.get_files(
        search_term, keywords_search, num_matches,
        job_name, path_base)

    files = path_functions.filter_paths(files, filter_word)
        
    files = path_functions.agg_paths_by_type2(files)

    for key, values in files.items():
        
        if key == 'html' and 'html' in types:
            #Convert
            df_html = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df = pd.concat([df, df_html])

        if key == 'bat' and 'bat' in types:
            #Convert
            df_bat = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df = pd.concat([df, df_bat])

        if key == 'pdf' and 'pdf' in types:
            #Convert
            df_pdfs = html_to_csv.load_and_convert_files(path_base, paths=values, format_type=key)
            df_pdfs = df_pdfs.drop_duplicates()
            df = pd.concat([df, df_pdfs])
            #Analyze

    if "Número Modalidade" in df.columns:
        df.drop(columns=["Número Modalidade"],inplace=True)

    #Analyze
    isvalid, column_modalidade = check_df.contains_keyword(df, word='modalidade')

    for index, value in df.iterrows():
        result['dispensa'].append(analyze_dispensa (value, column_modalidade))
            
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='dispensa', threshold=threshold)
        
    return isvalid, result

def predict_resultado(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index', threshold=0, pattern='/tmp/es/data'): 

    result = {'resultado': []}

    #Search
    html_files = indexing.get_files(
        search_term, keywords_search, num_matches,
        job_name, path_base)

    df = html_to_csv.load_and_convert_files(path_base, paths=html_files, format_type='html')

    #Analyze
    isvalid, column_modalidade = check_df.contains_keyword(df, word='resultado')

    if isvalid:
        result['resultado'].append(analyze_resultado (df, column_modalidade))
            
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='resultado', threshold=threshold)
    
    return isvalid, result

           
def predict_editais(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'editais': []}

    #Search
    html_files = indexing.get_files(
        search_term, keywords_search, num_matches,
        job_name, path_base)

    df = html_to_csv.load_and_convert_files(path_base, paths=html_files, format_type='html')

    #Analyze
    isvalid, column_edital = check_df.contains_keyword(df, word='editais')
    if isvalid:
        result['editais'].append(analyze_edital(df, column_edital))

    #Check
    isvalid = check_df.infos_isvalid(result, column_name='editais', threshold=threshold)
    
    return isvalid, result

def predict_busca(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'busca': []}

    #Search
    html_files = indexing.get_files_to_valid(
        search_term, keywords_search, num_matches,
        job_name, path_base, types=['html'])
    print(html_files)

    #Analyze
    result = check_all_files_busca(html_files, result)

    #Check
    isvalid = check_df.infos_isvalid(result, column_name='busca', threshold=threshold)
    
    return isvalid, result

def explain(df, column_name, verbose=False):

    result = "Explain - Quantidade entradas analizadas: {}\n\tQuantidade de entradas válidas: {}\n".format(
         len(df[column_name]), sum(df[column_name]))

    if verbose:
        print(result)

    return result

def explain_proc_lic(df, column_name, verbose=False):
    print(df)
    print("*******************************")
    print(column_name)
    result = ''

    # result = "Explain - Quantidade entradas analizadas: {}\n\tQuantidade de entradas válidas: {}\n".format(
    #      len(df[column_name]), sum(df[column_name]))

    # if verbose:
    #     print(result)

    return result



#path_base = "/home/cinthia/MPMG/persistence_area/"
#path_base = "C:/Users/ritar"
#path_base = "C:/Users/pedro"

