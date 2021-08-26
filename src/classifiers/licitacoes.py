from bs4 import BeautifulSoup
import pandas as pd
import constant
import re
import os
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, '../')
# sys.path.insert(0, '/home/cinthia/MPMG/F01/src')

from utils import indexing
from utils import table_to_csv
from utils import search_path_in_dump

def analyze_proc_lici(df, keywords): 
    """
    Verifica se existem colunas para cada palavra-chave e a quantidade de valores nulos
    em cada uma delas
    """

    val = { i: [] for i in keywords}

    for i in keywords:

        isvalid, column_name = search_path_in_dump.check_columns(df=df, word=i)

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

def check_result(df, column_name, threshold=0): 
    
    if sum(df[column_name]) > threshold:
        return True
    else:
        return False

def preprocess_paths(sorted_result, word):

    paths = search_path_in_dump.get_paths(sorted_result)
    paths = (sorted(set(paths)))
    paths = search_path_in_dump.filter_paths(paths, word)

    return paths

def agg_type(paths):

    files = {'csv': [], 'xls': [], 'html': [], 'pdf': [], 'doc':[]}

    for path in paths:

        suffix = Path(path).suffixes[0]
        print(suffix)

        if suffix == ".xls":
            files['xls'].append(path)
        elif suffix == '.csv':
            files['csv'].append(path)
        elif (suffix == ".html") or (suffix == '.xml'):
            files['html'].append(path)
        elif (suffix == ".pdf"):
            files['pdf'].append(path)
        elif (suffix == ".doc") or (suffix == '.docx'):
            files['doc'].append(path)

    return files

def concat_lists(files):

    if len(files) == 1:
        df = files[0]
    else:
        df = pd.concat(files)
    return df

def load_and_convert_files(path_base, paths, type):

    if type == 'html':
        
        if os.path.isfile("licitacoes.csv"):
            df = pd.read_csv("licitacoes.csv")
        else:
            df = search_path_in_dump.list_to_csv(paths, path_base, "licitacoes.csv")

    elif type == 'csv':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(path_base + i))

        df = concat_lists(list_csv)

    elif type == 'xls':

        list_xls = []
        for i in  paths:
            list_xls.append(pd.read_excel(path_base + i))

        df = concat_lists(list_xls)

    return df

def predict_proc_lic(
    search_term, keywords_search, path_base, num_matches=40,
    keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais'],
    filter_word='licitacoes', job_name='index_gv', threshold = 0): 

    result = {'proc_lic': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #paths = ['ipatinga/licitacoes_ipatinga/data/files/fddd90f7cb20075fb3c866c6ec307e07.xls']

    files = agg_type(paths)
    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = load_and_convert_files(path_base, paths=values, type=key)

            #Analyze
            result['proc_lic'] = analyze_proc_lici(df, keywords_check)

    #Check
    isvalid = []
    for i in keywords_check:
        isvalid.append(check_result(result['proc_lic'], i, threshold=threshold))

    return isvalid, result


def predict_inexigibilidade(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'inexigibilidade': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #paths = ['ipatinga/licitacoes_ipatinga/data/files/fddd90f7cb20075fb3c866c6ec307e07.xls']

    files = agg_type(paths)
    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = load_and_convert_files(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_modalidade = search_path_in_dump.check_columns(df, word='modalidade')
            if isvalid:
                for index, value in df.iterrows():
                    result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_result(result, column_name='inexigibilidade', threshold=threshold)
        
    return isvalid, result

def predict_resultado(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'resultado': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #paths = ['ipatinga/licitacoes_ipatinga/data/files/fddd90f7cb20075fb3c866c6ec307e07.xls']

    files = agg_type(paths)
    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = load_and_convert_files(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_modalidade = search_path_in_dump.check_columns(df, word='resultado')
            if isvalid:
                for index, value in df.iterrows():
                    result['resultado'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_result(result, column_name='resultado', threshold=threshold)
    
    return isvalid, result

def predict_dispensa(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'dispensa': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #paths = ['ipatinga/licitacoes_ipatinga/data/files/fddd90f7cb20075fb3c866c6ec307e07.xls']

    files = agg_type(paths)
    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = load_and_convert_files(path_base, paths=values, type=key)
    
            #Analyze
            isvalid, column_modalidade = search_path_in_dump.check_columns(df, word='dispensa')
            if isvalid:
                for index, value in df.iterrows():
                    result['dispensa'].append(analyze_inexibilidade (value, column_modalidade))
            
    #Check
    isvalid = check_result(result, column_name='dispensa', threshold=threshold)
    
    return isvalid, result
           
def predict_editais(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'editais': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #paths = ['ipatinga/licitacoes_ipatinga/data/files/fddd90f7cb20075fb3c866c6ec307e07.xls']

    files = agg_type(paths)
    for key, values in files.items():
        
        if (key == 'html') or (key == 'xls'):
            #Convert
            df = load_and_convert_files(path_base, paths=values, type=key)

            #Analyze
            isvalid, column_edital = search_path_in_dump.check_columns(df, word='editais')
            if isvalid:
                for index, value in df.iterrows():
                    result['editais'].append(analyze_edital(df, column_edital))

    #Check
    isvalid = check_result(result, column_name='editais', threshold=threshold)
    
    return isvalid, result

def predict_busca(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'busca': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #Analyze
    result = check_all_files_busca(paths, path_base, result)

    #Check
    isvalid = check_result(result, column_name='busca', threshold=threshold)
    
    return isvalid, result

def explain(df, column_name):

    print("Explain - Quantidade de arquivos analizados: {}\n\tQuantidade de aquivos válidos: {}\n".format(
         len(df[column_name]), sum(df[column_name])))


#path_base = "/home/cinthia/MPMG/persistence_area/"
    # path_base = "C:/Users/ritar"
path_base = "C:/Users/pedro"

