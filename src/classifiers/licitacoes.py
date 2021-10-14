from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import numpy as np
import sys

#sys.path.insert(0, '/home/cinthia/F01/src')

from pathlib import Path

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

        isvalid, column_name = check_df.check_columns(df=df, word=i)

        if isvalid:
            val[i] = list(~df[column_name].isna())
        else:
            val[i] = [False]
    
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

def analyze_busca(format_path):
    """
    Verifica se os documentos html possuem o campo "Filtrar Pesquisa"
    """

    try:
        soup = BeautifulSoup(open(format_path), features="lxml")
        text = soup.get_text()

        if re.search("filtrar\s*pesquisa", text, re.IGNORECASE) != None:
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
    if len(df[column_name].value_counts()) > 0:
        return True
    else:
        return False

def check_all_files_busca(paths, path_base, result):

    for path, type in paths:
        if type == 'html':
            files = os.listdir(path_base + "/" + path)
            for file in files:
                format_path = "{}/{}/{}".format(path_base, path, file)
                result['busca'].append(analyze_busca(format_path))

    return result


def predict_proc_lic(
    search_term, keywords_search, path_base, num_matches=40,
    keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais'],
    filter_word='licitacoes', job_name='index_gv', threshold = 0, pattern='/tmp/es/data'): 

    result = {'proc_lic': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = path_functions.preprocess_paths(sorted_result, word=filter_word)

    files = path_functions.agg_paths_by_type(paths)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = html_to_csv(path_base, paths=values, type=key)

            #Analyze
            result['proc_lic'] = analyze_proc_lici(df, keywords_check)

    #Check
    isvalid = []
    for i in keywords_check:
        isvalid.append(check_df.infos_isvalid(result['proc_lic'], i, threshold=threshold))

    return isvalid, result


def predict_inexigibilidade(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'inexigibilidade': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = path_functions.preprocess_paths(sorted_result, word=filter_word)

    files = path_functions.agg_paths_by_type(paths)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = html_to_csv(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_modalidade = check_df.contains_keyword(df, word='modalidade')
            if isvalid:
                for index, value in df.iterrows():
                    result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='inexigibilidade', threshold=threshold)
        
    return isvalid, result

def predict_resultado(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'resultado': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = path_functions.preprocess_paths(sorted_result, word=filter_word)

    files = path_functions.agg_paths_by_type(paths)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = html_to_csv(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_modalidade = check_df.contains_keyword(df, word='resultado')
            if isvalid:
                for index, value in df.iterrows():
                    result['resultado'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='resultado', threshold=threshold)
    
    return isvalid, result

def predict_dispensa(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'dispensa': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = path_functions.preprocess_paths(sorted_result, word=filter_word)

    files = path_functions.agg_paths_by_type(paths)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = html_to_csv(path_base, paths=values, type=key)
    
            #Analyze
            isvalid, column_modalidade = check_df.contains_keyword(df, word='dispensa')
            if isvalid:
                for index, value in df.iterrows():
                    result['dispensa'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_df.infos_isvalid(result, column_name='dispensa', threshold=threshold)
    
    return isvalid, result
           
def predict_editais(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'editais': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = path_functions.preprocess_paths(sorted_result, word=filter_word)

    files = path_functions.agg_paths_by_type(paths)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = html_to_csv(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_edital = check_df.contains_keyword(df, word='editais')
            if isvalid:
                for index, value in df.iterrows():
                    result['editais'].append(analyze_edital(df, column_edital))

    #Check
    isvalid = check_df.infos_isvalid(result, column_name='editais', threshold=threshold)
    
    return isvalid, result

def predict_busca(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0, pattern='/tmp/es/data'): 

    result = {'busca': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    files = path_functions.preprocess_paths(sorted_result, word=filter_word)

    if pattern != "":
        files = path_functions.create_valid_path (files, path_base=path_base, pattern=pattern)

    #Analyze
    result = path_functions.check_all_files_busca(files, path_base, result)

    #Check
    isvalid = check_df.infos_isvalid(result, column_name='busca', threshold=threshold)
    
    return isvalid, result

def explain(df, column_name, verbose=False):

    result = "Explain - Quantidade de arquivos analizados: {}\n\tQuantidade de aquivos válidos: {}\n".format(
         len(df[column_name]), sum(df[column_name]))

    if verbose:
        print(result)

    return result


#path_base = "/home/cinthia/MPMG/persistence_area/"
#path_base = "C:/Users/ritar"
#path_base = "C:/Users/pedro"

