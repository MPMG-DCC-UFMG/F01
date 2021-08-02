import sys, constant, unidecode
import pandas as pd

sys.path.insert(1, '../')

from utils import singlepage_to_csv

checklist_viagens = {
    'nome':False,
    'cargo':False,
    'valor_total':False,
    'periodo':False,
    'destino':False,
    'atividade':False,
    'num_diarias':False,
}

expected_type = {
    'nome':'str',
    'cargo':'str',
    'valor_total':'int',
    'periodo':'str',
    'destino':'str',
    'atividade':'str',
    'num_diarias':'int',
}

filepath = "../../Governador Valadares/despesas-por-diarias/despesas_por_diarias_1.html"

def search_keywords_diaria_viagem(df):
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

def predict_diaria_viagem():

    df = singlepage_to_csv.convert(filepath)
    search_keywords_diaria_viagem(df)    
    checklist_viagens['len_df'] = df.shape[0]
    prediction = True
    for value in checklist_viagens.values():
        if(not value): 
            prediction = False
            break

    print("\nPrediction Copia Digital Edital:", prediction)

    return checklist_viagens

def explain_diaria_viagem(dict_diaria_viagem):
   print("\n")
   for key in dict_diaria_viagem.keys():
        if key == 'len_df': continue
        if dict_diaria_viagem[key]:
            print("Foi encontrada a seguinte coluna para", key, ":", dict_diaria_viagem[key][0], "e", round(100* dict_diaria_viagem[key][1]/checklist_viagens['len_df'], 2), "% da coluna está preenchida.")
        else: 
           print("Não foi encontrada nenhuma referência a", key)
   print("\n")

