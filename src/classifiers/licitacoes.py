from bs4 import BeautifulSoup
import pandas as pd
import constant
import re
import os
import numpy as np
import sys
sys.path.insert(0, '/home/cinthia/MPMG/F01/src')

from utils import indexing
from utils import table_to_csv

def get_extension(path):
    return path.split('.')[-1]

def  format_path(path):
    path = path.split("/")
    return "/".join(path[3: len(path)-1])

def get_paths(indexes):

    paths = []

    for i in indexes:

        extensions = get_extension(str(i[2]))
        path = format_path (str(i[2]))
        paths.append((path, extensions))

    return paths

def check_columns(df, word):
    """
    Verifica se um dataframe possui uma coluna cujo nome contém uma palavra-chave
    """

    columns = [i.lower() for i in df.columns]
    i = 0
    for column_name in columns:

        finder = column_name.find(word)
       
        if finder != -1:
            return True, columns[i]
    
        i +=1
    return False, word


def filter_paths(paths, word="licitacoes"):
    """
    Filtra os caminhos retornados pelo indexador por uma palavra-chave
    """

    filtered_paths = []
    for i in paths:

        if i[0].find(word) != -1:
            filtered_paths.append(i)
    
    return filtered_paths

def one_list_to_csv (format_path):
    """
    Convert um elemento 'li' do html para um dataframe.
    """

    try: 

        df, type = table_to_csv.convert_one_file(format_path)

        if type == 'list':
            return df
        
    except ValueError:
        pass

    return df

def list_to_csv(paths, path_base):

    list_df = []

    for path, type in paths:
        
        if type == 'html':
            files = os.listdir(path_base + "/" + path)
            for file in files:
                format_path = "{}/{}/{}".format(path_base, path, file)
                if not os.path.isfile("licitacoes.csv"):
                    list_df.append(one_list_to_csv (format_path))

    return pd.concat(list_df)

def analyze_proc_lici(df, keywords): 
    """
    Verifica se existem colunas para cada palavra-chave e a quantidade de valores nulos
    em cada uma delas
    """

    val = { i: [] for i in keywords}

    for i in keywords:

        isvalid, column_name = check_columns(df=df, word=i)

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

    soup = BeautifulSoup(open(format_path), features="lxml")
    text = soup.get_text()

    if re.search("filtrar\s*pesquisa", text, re.IGNORECASE) != None:
        return True

    return False

def analyze_edital(df, column_name):
    """
    Verifica se na coluna Editais há algum arquivo
    """

    if len(df[column_name].value_counts()) > 0:
        return True
    else:
        return False


def predict(df, column_name, threshold = 0): 
    
    if sum(df[column_name]) > threshold:
        return True
    else:
        return False

def explain(df, column_name):

    print("Quantidade de arquivos analizados: {}\n Quantidade de aquivos válidos {}\n".format(
         len(df[column_name]), sum(df[column_name])))


def check_all_files_busca(paths, path_base, result):

    for path, type in paths:
        if type == 'html':
            files = os.listdir(path_base + "/" + path)
            for file in files:
                format_path = "{}/{}/{}".format(path_base, path, file)
                result['busca'].append(analyze_busca(format_path))

    return result


def main (path_base):

    search_term="Licitações"
    keywords = ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ]

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords, num_matches= 10, job_name="index_gv")

    paths = get_paths(sorted_result)
    paths = (sorted(set(paths)))
    paths = filter_paths(paths, word="licitacoes")
    print(paths)

    result = {'proc_lic': [], 'inexigibilidade': [], 'busca': [] , 'edital': []}
    keywords = ['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais']

    #Converte lista em html para csv
    if os.path.isfile("licitacoes.csv"):
        df = pd.read_csv("licitacoes.csv")
    else:
        df = list_to_csv(paths, path_base)

    # procedimentos licitatórios
    result['proc_lic'] = analyze_proc_lici(df, keywords)
    for i in keywords:
        print("Procedimentos Licitatórios - {}: {}".format(i, predict(result['proc_lic'], i)))
        print(explain(result['proc_lic'], i))

    isvalid, column_modalidade = check_columns(df, word='modalidade')
    isvalid, column_edital = check_columns(df, word='editais')
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
    print(explain(result, 'explain'))


#local onde está o dump
path_base = "/home/cinthia/MPMG/persistence_area"
main (path_base)
