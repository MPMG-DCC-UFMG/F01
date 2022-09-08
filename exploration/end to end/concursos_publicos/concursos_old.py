import os, re, codecs, sys, utilconst.constant as constant
sys.path.insert(1, '../')

from bs4 import BeautifulSoup


home_path = "../../Governador Valadares/home/home.html"
file_path = '../../Governador Valadares/downloads/categoria/ConcursoPublico-EditalNo00120190022019e0032019.html'

from src.validadores.utils import indexing


def search_keywords_dados_concurso(markup):

    status = None
    resultado = None
    nomeacao = None
    for div in markup.find_all('div', {"class": "list-group"}):
        for key in constant.CHECKLIST_CONCURSO_SEARCH['status']:
            ref = div.find(text = re.compile('.*({}).*'.format(key)))
            if(ref): 
                status = ref
                break
        for key in constant.CHECKLIST_CONCURSO_SEARCH['resultado']:
            ref = div.find(text = re.compile('.*({}).*'.format(key)))
            if(ref): 
                resultado = ref
                break
        
        ref = div.find(text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['nomeacao'])))
        if(ref): nomeacao = ref
            
        if (status and resultado and nomeacao): return [status, resultado, nomeacao]

    return [status, resultado, nomeacao]


def get_files_by_keyword(search_term, keywords):

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords=keywords, num_matches= 10, job_name="index_gv")

    files = [file[2] for file in sorted_result if file[2].endswith('html')]

    for f in sorted_result:
        print(f, '\n')

    return files

def predict_dados_concurso():

    files = get_files_by_keyword(constant.CONCURSO_PUBLICO, constant.CONCURSO_PUBLICO_KEYWORDS)    
    # markup =  BeautifulSoup(codecs.open(file_path, 'r', 'utf-8').read(),  "html.parser" )
    # search_keywords_dados_concurso(markup)
    
    # dados_concurso = search_keywords_dados_concurso(markup)
    # classifier =  dados_concurso is not None
    
    # print("\nPrediction Dados Concurso:", classifier)
    # ans = {
    #     'status': dados_concurso[0], 
    #     'resultado': dados_concurso[1], 
    #     'nomeacao': dados_concurso[2],
    #     'classifier': classifier 
    # }

    # return ans



def explain_dados_concurso(dados_concurso):

    if(dados_concurso['status']): print("\nFoi encontrada uma referência a Status do Andamento do concurso:", dados_concurso['status'])
    else: print("\nNão foi encontrada uma referência a Status do Andamento do concurso")
    
    if(dados_concurso['resultado']): print("Foi encontrada uma referência a Resultado de concursos:", dados_concurso['resultado'])
    else: print("Não foi encontrada uma referência a Resultado de concursos")
    
    if(dados_concurso['nomeacao']): print("Foi encontrada uma referência a Nomeação:", dados_concurso['nomeacao'])
    else:  print("Não foi encontrada uma referência a Nomeação")


# -------------------------------------------------------------------- Copia Digital ----------------------------------------------------------------------------

def search_keywords_copia_digital(markup):
    for div in markup.find_all('div', {"class": "list-group"}):
        for key in constant.CHECKLIST_CONCURSO_SEARCH['copia_digital']:
            if(div.find("h4", text = re.compile('.*({}).*'.format(key)))): 
                for link in div.find_all(href=True):
                    if('pdf' in link['href']):    
                        return link['href']


def predict_copia_edital():
    markup =  BeautifulSoup(codecs.open(file_path, 'r', 'utf-8') .read(),  "html.parser" )
    
    copia_digital = search_keywords_copia_digital(markup)
    classifier =  copia_digital is not None
    
    print("\nPrediction Copia Digital Edital:", classifier)
    ans = {
        'copia_digital': copia_digital,
        'classifier': classifier 
    }

    return ans

def explain_copia_edital(dict_copia_edital):
    
    if(dict_copia_edital['classifier']): print("\nFoi encontrada uma referência a copia digital:", dict_copia_edital['copia_digital'])
    else: print("\nNão foi encontrada uma referência a copia digital do edital")
    
# ------------------------------------------------------------- Recursos -----------------------------------------------------------------------------------

def search_keywords_recursos(markup):
    divulgacao = None
    decisoes = None

    for div in markup.find_all('div', {"class": "list-group"}):
        ref = div.find("h4", text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['recursos'][0])))
        if(ref): divulgacao = ref.getText()
        
        ref = div.find("h4", text = re.compile('.*({}).*'.format(constant.CHECKLIST_CONCURSO_SEARCH['recursos'][1])))
        if(ref): decisoes = ref.getText()
            
        if (divulgacao and decisoes): break
    
    return divulgacao, decisoes

def predict_recursos(): 
    markup =  BeautifulSoup(codecs.open(file_path, 'r', 'utf-8') .read(),  "html.parser" )
    divulgacao, decisoes = search_keywords_recursos(markup)
    classifier =  divulgacao is not None and decisoes is not None
    
    print("\nPrediction Recursos:", classifier)
    ans = {
        'divulgacao': divulgacao,
        'decisoes': decisoes,
        'classifier': classifier 
    }

    return ans

def explain_recursos(dict_recursos):
   
    if dict_recursos['classifier']:
        if(dict_recursos['divulgacao']): print("\nFoi encontrada uma referência a divulgação de recursos:", dict_recursos['divulgacao'])
        else: print("\nNão foi encontrada uma referência a divulgação de recursos")
        
        if(dict_recursos['decisoes']): print("\nFoi encontrada uma referência aos resultados dos recursos:", dict_recursos['decisoes'])
        else: print("\nNão foi encontrada uma referência aos resultados dos recursos")

    else: 
        if dict_recursos['divulgacao'] is None:
            print("\nNão foi encontrada referência a divulgação de recursos:")
        if dict_recursos['decisoes'] is None:
            print("\nNão foi encontrada referência a decisão de recursos:")
