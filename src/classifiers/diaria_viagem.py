import os, sys, requests, codecs, constant, unidecode, re, math
import pandas as pd

sys.path.insert(1, '../')

from utils import table_to_csv
from bs4 import BeautifulSoup

checklist_viagens = {
    'nome':False,
    'cargo':False,
    'destino':False,
    'atividade':False,
    'periodo':False,
    'num_diarias':False,
    'valor_total':False,
    'base_legal':False
}

expected_type = {
    'nome':'str',
    'cargo':'str',
    'destino':'str',
    'atividade':'str',
    'periodo':'str',
    'num_diarias':'int',
    'valor_total':'int',
    'base_legal':'str'
}


#iterates through files 
def predict_diaria_viagem():

    path = "../../Governador Valadares"
    folder = 'despesas-por-diarias'
    
    possible_urls = get_possible_urls()
    
    if(possible_urls):    
        all_files = os.listdir("{}/{}".format(path, folder))
        df = table_to_csv.convert(all_files, path, folder)

        for header in df.head(): #for each header
            for item in constant.CHECKLIST_VIAGEM_SEARCH: #search for each checklist item
                for key in constant.CHECKLIST_VIAGEM_SEARCH[item]: # search for key word
                    if key in unidecode.unidecode(header).lower():  #if key word is in header
                        if(expected_type[item] == 'int'):
                            new_list = [ l for l in df[header] if ((not pd.isnull(l)) and any(c.isdigit() for c in l))]
                            checklist_viagens[item] = [header, len(new_list)]   
                        else:    
                            new_list = [l for l in df[header] if (not pd.isnull(l))]
                            checklist_viagens[item] = [header, len(new_list)]
    return df

def get_possible_urls():
    path = "../../Governador Valadares"
    home_dir = "/home/home.html"
    file = codecs.open(path + home_dir, 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    possible_urls = []
    
    for elem in html.find_all(href=True):
        for s in constant.DIARIA_VIAGEM: 
            if s in elem.getText():
                possible_urls.append(elem['href'])
    return possible_urls

def explain_diaria_viagem(df):

    classifier = True
    for key in checklist_viagens.keys():
        if checklist_viagens[key]:
            pass
        else:
            classifier = False

    print("\nPrediction diaria: \n", classifier)
    len_df = float('inf')
    len_df = df.shape[0]
    for key in checklist_viagens.keys():
            if checklist_viagens[key]:
                print("Foi encontrada a seguinte coluna para", key, ":", checklist_viagens[key][0], "e", round(100* checklist_viagens[key][1]/len_df, 2), "% da coluna está preenchida.")
            else: 
                print("Não foi encontrada nenhuma referência a", key)
    print("\n")

