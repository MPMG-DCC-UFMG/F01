import os, re, codecs, requests, sys, constant
sys.path.insert(1, '../')

from bs4 import BeautifulSoup
from utils import search_in_home


home_path = "../../../../Governador Valadares/home/home.html"
file_path = '../../../../Governador Valadares/downloads/categoria/ConcursoPublico-EditalNo00120190022019e0032019.html'

checklist_concursos = {
    'copia_digital':False,
    'status':False,
    'recursos':[False, False],
    'resultado': False,
    'nomeacao':False
}

def get_markup():
    #missing indexing :p
    
    file = codecs.open(file_path, 'r', 'utf-8')    
    return BeautifulSoup(file.read(),  "html.parser" )

def predict_dados_concurso(markup):
    
    for div in markup.find_all('div', {"class": "list-group"}):
    
        for key in constant.CHECKLIST_CONCURSO_SEARCH['status']:
            ref = div.find(text = re.compile('.*({}).*'.format(key)))
            if(ref): 
                checklist_concursos['status'] = ref
                break
        for key in constant.CHECKLIST_CONCURSO_SEARCH['resultado']:
            ref = div.find(text = re.compile('.*({}).*'.format(key)))
            if(ref): 
                checklist_concursos['resultado'] = ref
                break
        ref = div.find(text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['nomeacao'])))
        if(ref): checklist_concursos['nomeacao'] = ref
            
        if (checklist_concursos['status'] and checklist_concursos['resultado'] and checklist_concursos['nomeacao']): return True

    return False


def explain_dados_concurso():

    if(checklist_concursos['status']): print("\nFoi encontrada uma referência a Status do Andamento do concurso:", checklist_concursos['status'])
    else: print("\nNão foi encontrada uma referência a Status do Andamento do concurso")
    
    if(checklist_concursos['resultado']): print("Foi encontrada uma referência a Resultado de concursos:", checklist_concursos['resultado'])
    else: print("Não foi encontrada uma referência a Resultado de concursos")
    
    if(checklist_concursos['nomeacao']): print("Foi encontrada uma referência a Nomeação:", checklist_concursos['nomeacao'])
    else:  print("Não foi encontrada uma referência a Nomeação")


def predict_copia_edital(markup):

    for div in markup.find_all('div', {"class": "list-group"}):
        for key in constant.CHECKLIST_CONCURSO_SEARCH['copia_digital']:
            if(div.find("h4", text = re.compile('.*({}).*'.format(key)))): 
                for link in div.find_all(href=True):
                    print(link['href'])
                    if('pdf' in link['href']):    
                        checklist_concursos['copia_digital'] = link['href']
                        break
            
        if (checklist_concursos['copia_digital']): return True

    return False

def explain_copia_edital():
    
    if(checklist_concursos['copia_digital']): print("\nFoi encontrada uma referência a copia digital:", checklist_concursos['copia_digital'])
    else: print("\nNão foi encontrada uma referência a copia digital do edital")
    
def predict_recursos(markup):
    
    for div in markup.find_all('div', {"class": "list-group"}):
        ref = div.find("h4", text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['recursos'][0])))
        if(ref): checklist_concursos['recursos'][0] = ref.getText()
        
        ref = div.find("h4", text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['recursos'][1])))
        if(ref): checklist_concursos['recursos'][1] = ref.getText()
            
        if (checklist_concursos['recursos'][0] and checklist_concursos['recursos'][1]): return True

    return False

def explain_recursos():
   
    if(checklist_concursos['recursos'][0]): print("\nFoi encontrada uma referência a divulgação de recursos:", checklist_concursos['recursos'][0])
    else: print("\nNão foi encontrada uma referência a divulgação de recursos")
    
    if(checklist_concursos['recursos'][1]): print("\nFoi encontrada uma referência aos resultados dos recursos:", checklist_concursos['recursos'][1])
    else: print("\nNão foi encontrada uma referência aos resultados dos recursos")
    
    
# predict_dados_concurso(get_markup())
# explain_dados_concurso()

# predict_copia_edital(get_markup())
# explain_copia_edital()

# predict_recursos(get_markup())
# explain_recursos()