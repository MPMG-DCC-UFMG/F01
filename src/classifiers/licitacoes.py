from bs4 import BeautifulSoup
import pandas as pd
import codecs
import constant
import re
from os import walk

def search_pages(object, keyword):
    #Not working yet
    return

#--------------------------------------------------------Processos licitatórios--------------------------------------------------------
# Registro das licitações realizadas pela Prefeitura, Câmara Municipal Ou Adm Indireta:
#  organizado, preferencialmente, conforme o momento da licitação (em andamento ou concluída);
#  a ordem cronológica e numérica (número do procedimento) e o tipo de procedimento

licitacoes_dict = {
    "numero-ano_do_edital": False,
    "modalidade": False,
    "objeto": False,
    'situacao-status': {'value': False, 'expĺain': "Possível organizar conforme a situação, momentos"},
}

ordenacao_licitacoes = {
    'ordem': {'value': False, 'expĺain': "Possível organizar nas seguintes ordens"},
    'tipo': {'value':False, 'expĺain': "Possível diferenciar o tipo de procedimento"}
}

#Busca por organizar conforme a situação: em andamento ou concluída
def check_for_situacao(html):
    match_word = []
    for word in constant.ORDEM_LICITACOES["situacao"]:
        selects = html.find_all(text = re.compile("^"+ word +"$", re.IGNORECASE))
        if selects: match_word.append(word)
    return match_word       

def check_for_tipo(html):
    match_word = []
    for word in constant.ORDEM_LICITACOES["tipo"]:
        selects = html.find(text=re.compile("^"+ word +"$", re.IGNORECASE))
        if selects:match_word.append(word)
    return match_word     

def predict__licitacoes():
    
    filename = '../../Governador Valadares/licitacoes/licitacoes.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )

    ordenacao_licitacoes["situacao"]["value"] = check_for_situacao(html) 

    match_word = []
    for word in constant.ORDEM_LICITACOES["ordem"]:
        selects = html.find(text=re.compile("^"+ word +"$", re.IGNORECASE))
        if selects: match_word.append(word)
    ordenacao_licitacoes["ordem"]["value"] = match_word     


    match_word = []
    for word in constant.ORDEM_LICITACOES["tipo"]:
        selects = html.find(text=re.compile("^"+ word +"$", re.IGNORECASE))
        if selects:match_word.append(word)
    ordenacao_licitacoes["tipo"]["value"] =  match_word 

    return ordenacao_licitacoes

def explain_licitacoes(ordenacao_licitacoes):
    print("\n", "Explain Licitacoes: ----------------------" ,"\n")
    for item in ordenacao_licitacoes:
        # print(item.explain, ": ", item.value)
        print(ordenacao_licitacoes[item]["expĺain"] + ": ",ordenacao_licitacoes[item]["value"], "\n")




def predict_inexigibilidade_dispensa():
    pass

def predict_processoslicitatorios():
    pass


def predict_editais():
    # Disponibiliza o conteúdo integral dos editais	
    pass
def explain_editais():
    # Disponibiliza o conteúdo integral dos editais	
    pass

def predict_resultado():
    # Possibilita a consulta aos resultados das licitações ocorridas	
    pass
def explain_resultado():
    # Possibilita a consulta aos resultados das licitações ocorridas	
    pass

