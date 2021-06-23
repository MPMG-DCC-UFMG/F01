from bs4 import BeautifulSoup
import pandas as pd
import codecs
import constant
import re
from os import walk

# Registro das licitações realizadas pela Prefeitura, Câmara Municipal Ou Adm Indireta:
#  organizado, preferencialmente, conforme o momento da licitação (em andamento ou concluída);
#  a ordem cronológica e numérica (número do procedimento) e o tipo de procedimento

licitacoes = {
    'registro': {'value': False, 'expĺain': "Registro de licitações foram encontrados"},
    'situacao': {'value': False, 'expĺain': "Possível organizar conforme os momentos"},
    'ordem': {'value': False, 'expĺain': "Possível organizar nas seguintes ordens"},
    'tipo': {'value':False, 'expĺain': "Possível diferenciar o tipo de procedimento"}
}

#Tag item exists in Home
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.LICITACOES, href=True)

def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

#Verifica se contém alguma licitação
def check_for_registro(html):
    dir = "./Governador Valadares/licitacoes"
    filenames = get_all_filenames_in_dir(dir)
    if filenames: return True
    else: return False

#Busca por organizar conforme a situação: em andamento ou concluída
def check_for_situacao(html):
    match_word = []
    for word in constant.ORDEM_LICITACOES["situacao"]:
        selects = html.find_all(text = re.compile("^"+ word +"$", re.IGNORECASE))
        if selects: match_word.append(word)
    return match_word     

#Searches for sorting elements
def check_for_ordem(html):
    match_word = []
    for word in constant.ORDEM_LICITACOES["ordem"]:
        selects = html.find(text=re.compile("^"+ word +"$", re.IGNORECASE))
        if selects: match_word.append(word)
    return match_word     

def check_for_tipo(html):
    match_word = []
    for word in constant.ORDEM_LICITACOES["tipo"]:
        selects = html.find(text=re.compile("^"+ word +"$", re.IGNORECASE))
        if selects:match_word.append(word)
    return match_word     


def predict_licitacoes (html):

    licitacoes["registro"]["value"] = check_for_registro(html)
    licitacoes["situacao"]["value"] = check_for_situacao(html) 
    licitacoes["ordem"]["value"] = check_for_ordem(html)
    licitacoes["tipo"]["value"] = check_for_tipo(html)

    if (licitacoes["registro"]["value"]):
        return True
    return False

def explain(macro):

    print("\n", "Explain:" ,"\n")

    if(macro is None):
        print("Não foi encontrado na página principal do portal um link que possua como valor textual alguma das seguintes palavras chave:")
        for fs in constant.LICITACOES:
            print(fs, ' ')
    else:
        for item in licitacoes:
            # print(item.explain, ": ", item.value)
            print(licitacoes[item]["expĺain"] + ": ",licitacoes[item]["value"], "\n")

def main():
    macro = get_macro()
    print(macro)
    if(not macro):  
        prediction = False 
    else:

        filename = './Governador Valadares/licitacoes/licitacoes.html'   
        file = codecs.open(filename, 'r', 'utf-8')
        html = BeautifulSoup(file.read(),  "html.parser" )

        prediction = predict_licitacoes(html)

    print("Predict Licitações: ", prediction, "\n")

    explain(macro)


main()