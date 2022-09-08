from bs4 import BeautifulSoup
import codecs, re
import pandas as pd
from utils import indexing
from utils import read
from utils import path_functions
import sys
sys.path.insert(1, '../')

from validadores import constant
from os import walk


#--------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------- Bases de dados abertos ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#


# Publica na internete relação das bases de dados abertos do município ou do estado

def search_keywords_dados_abertos(markup):
    api = []
    for a in markup.find_all("a", href = True):
        for keyword in constant.DADOS_ABERTOS:
            if keyword in a.getText():
                api.append(a)

    return api


def predict_bases_de_dados_abertos(search_term='Dados abertos', keywords=['dados abertos', 'API', 'divulgação'], 
    path_base = '/home', num_matches = 60, job_name = ''):

    #Search all files using keywords
    paths_html = indexing.get_files_to_valid( search_term, keywords, num_matches, job_name, path_base)

    result = []

    for filename in paths_html:
        # print(path_functions.get_url(path_base, filename), filename)
        try:
            file = codecs.open(filename, 'r', 'utf-8')
            markup = BeautifulSoup(file.read(),  "html.parser" )
        except:
            file = codecs.open(filename, 'r', 'latin-1')
            markup = BeautifulSoup(file.read(),  "html.parser" )
        macro = search_keywords_dados_abertos(markup)
        if (len(macro) != 0):
            result.append({'filename': filename, 'url': path_functions.get_url(path_base, filename), 'macro': macro})

    if (len(result) > 0):
        return True, result

    return False,result

def explain_bases_de_dados_abertos(isvalid, result):
    if isvalid :  
        result_explain = ('Nas seguintes páginas foram encontrados os seguintes elementos:')
        for res in result:
            result_explain = (result_explain, '; Página: ', res['filename'] + ', ' + res['url'] + '; Elemento: ', res['macro'])

    else:     
        result_explain = ("Nenhuma das palavras chave a seguir foram encontradas nas páginas direcionadas pelo indexador: ")
        for fs in constant.DADOS_ABERTOS:
            result_explain = result_explain + ', ' + fs
    
    return result_explain
