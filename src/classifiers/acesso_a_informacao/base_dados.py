from bs4 import BeautifulSoup
import codecs, re
from utils import indexing
from utils import path_functions
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

import constant
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
    path_base = '/home', num_matches = 30, job_name = ''):

    sorted_result = indexing.request_search(
      search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    path = [i[2] for i in sorted_result]
    path_html = path_functions.agg_paths_by_type(path)["html"]

    result = []

    for filename in path_html:
        # print(filename)
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
    print("PREDICTION Base de dados abertos:", isvalid) 
    if isvalid :  
        print('Nas seguintes páginas foram encontrados os seguintes elementos:')
        for res in result:
            print('Página:', res['filename'] + ', ' + res['url'], '\n\tElemento:', res['macro'])

    elif isvalid is False:     
        print("\nNenhuma das palavras chave a seguir foram encontradas nas páginas direcionadas pelo indexador:")
        for fs in constant.FAQ_SEARCH:
            print(fs, ' ')
