from bs4 import BeautifulSoup
import codecs, re

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

import constant
from os import walk


#--------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------- Bases de dados abertos ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

def search_keywords_dados_abertos(markup):
    api = []
    for a in markup.find_all("a", href = True):
        for keyword in constant.DADOS_ABERTOS:
            if keyword in a.getText():
                api.append(a['href'])

    return api

def predict_bases_de_dados_abertos():
    # Publica na internete relação das bases de dados abertos do município ou do estado
    filename = '../../../../Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
    ans = search_keywords_dados_abertos(markup)

    classifier = ans is not None
    print("Prediction Base de Dados:", classifier)
    ans = {
        'links': ans,
        'classifier': classifier 
    }
    return ans

