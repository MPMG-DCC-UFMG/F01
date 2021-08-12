from bs4 import BeautifulSoup
import pandas as pd
import constant
import re
import os
import numpy as np
import sys

sys.path.insert(0, '../')
#sys.path.insert(0, '/home/cinthia/MPMG/F01/src')

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
            val[i] = [False]*len(df[column_name])
    
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

def predict_proc_lic(
    search_term, keywords_search, path_base, num_matches=40,
    keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais'],
    filter_word='licitacoes', job_name='index_gv', threshold = 0): 

    result = {'proc_lic': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #Convert
    if os.path.isfile("licitacoes.csv"):
        df = pd.read_csv("licitacoes.csv")
    else:
        df = search_path_in_dump.list_to_csv(paths, path_base, "licitacoes.csv")

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

    #Convert
    if os.path.isfile("licitacoes.csv"):
        df = pd.read_csv("licitacoes.csv")
    else:
        df = search_path_in_dump.list_to_csv(paths, path_base, "licitacoes.csv")

    #Analyze
    isvalid, column_modalidade = search_path_in_dump.check_columns(df, word='modalidade')
    if isvalid:
        for index, value in df.iterrows():
            result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))
    
    #Check
    isvalid = check_result(result, column_name='inexigibilidade', threshold=threshold)
    
    return isvalid, result

def predict_editais(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0): 

    result = {'editais': []}

    #Search
    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords_search, num_matches=num_matches, job_name=job_name)
    paths = preprocess_paths(sorted_result, word=filter_word)

    #Convert
    if os.path.isfile("licitacoes.csv"):
        df = pd.read_csv("licitacoes.csv")
    else:
        df = search_path_in_dump.list_to_csv(paths, path_base, "licitacoes.csv")

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


"""def main (path_base):

    search_term="Licitações"
    keywords = ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ]

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords, num_matches= 40, job_name="index_gv")
    
    paths = search_path_in_dump.get_paths(sorted_result)
    paths = (sorted(set(paths)))
    paths = search_path_in_dump.filter_paths(paths, word="licitacoes")
    
    result = {'proc_lic': [], 'inexigibilidade': [], 'busca': [] , 'edital': []}
    keywords = ['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais']

    #Converte lista em html para csv
    if os.path.isfile("licitacoes.csv"):
        df = pd.read_csv("licitacoes.csv")
    else:
        df = search_path_in_dump.list_to_csv(paths, path_base, "licitacoes.csv")
        
    # procedimentos licitatórios
    result['proc_lic'] = analyze_proc_lici(df, keywords)
    for i in keywords:
        print("Procedimentos Licitatórios - {}: {}".format(i, predict(result['proc_lic'], i)))
        print(explain(result['proc_lic'], i))

    isvalid, column_modalidade = search_path_in_dump.check_columns(df, word='modalidade')
    isvalid, column_edital = search_path_in_dump.check_columns(df, word='editais')
    if isvalid:
        for index, value in df.iterrows():
            result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))
            result['edital'].append(analyze_edital(df, column_edital))


    # Inexigibilidade
    print("Inexigibilidade: {}".format(predict(result, 'inexigibilidade', threshold = 0)))
    print(explain(result, 'inexigibilidade'))

    #Edital
    print("Pública Edital: {}".format(predict(result, 'edital', threshold = 0)))
    print(explain(result, 'edital'))

    #Busca
    result = check_all_files_busca(paths, path_base, result)
    print("Permite Busca: {}".format(predict(result, 'busca', threshold = 0)))
    print(explain(result, 'busca'))"""


"""#local onde está o dump
path_base = "/home/cinthia/MPMG/persistence_area"
# path_base = "C:/Users/ritar"

#main (path_base)

search_term="Licitações"
keywords_search = ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ]

keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais']

isvalid, result = predict_proc_lic(
    search_term, keywords_search, path_base, num_matches=40,
    keywords_check=keywords_check,
    filter_word='licitacoes', job_name='index_gv', threshold = 0)


for i in range(len(keywords_check)):
  print("Predict - Procedimentos Licitatórios - {}: {}".format(keywords_check[i], isvalid[i]))
  print(explain(result['proc_lic'], keywords_check[i]))

isvalid, result = predict_inexigibilidade(
    search_term, keywords_search, path_base, num_matches=40,
     filter_word='licitacoes', job_name='index_gv', threshold=0)

print("Predict - Inexigibilidade: {}".format(isvalid))
print(explain(result, 'inexigibilidade'))

isvalid, result = predict_editais(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0)

print("Predict - Editais: {}".format(isvalid))
print(explain(result, 'editais'))

isvalid, result = predict_busca(
    search_term, keywords_search, path_base, num_matches=40,
    filter_word='licitacoes', job_name='index_gv', threshold=0)

print("Predict - Busca: {}".format(isvalid))
print(explain(result, 'busca'))"""