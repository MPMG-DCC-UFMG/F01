import os, re, codecs, requests
import requests
import constant
from bs4 import BeautifulSoup


checklist_concursos = {
    'registro': False,
    'copia_digital':False,
    'detalhes_andamento':False,
    'recursos':False,
    'resultado':False,
    'nomeacao':False
}

def validate_file(url):
    try:
        request = requests.get(url)
        #print('Trying to reach file', url)
        if request.status_code < 400:  
            return True

    except (requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
            requests.exceptions.TooManyRedirects, 
            TimeoutError):
        
        print("Failed to connect to ", url)
        return False

def get_title(markup):
    for c in constant.CONCURSO_PUBLICO:
        title = markup.find(text=(re.compile(r'^{}'.format(c))))
        if(title): return title
    
    return None

def search_in_dump(markup, item, search):
    title = get_title(markup)
    
    for div in markup.find_all('div', {"class": "list-group"}):
        checklist_concursos['registro'] = title
        link = constant.URL + div.find('a', href = True)['href']
        for s in search:
            if(s in div.find('h4').getText() and validate_file(link)):  
                checklist_concursos[item] = div.find('h4').getText()
                return
        
def link_to_dir(urls):
    return 'downloads/categoria/ConcursoPublico-EditalNo00120190022019e0032019.html'

def validate_items(url):
    
    dir = link_to_dir(url)

    if os.path.exists('./Governador Valadares/' + dir):
        html = BeautifulSoup(codecs.open('./Governador Valadares/' + dir, 'r', 'utf-8').read(),  "html.parser" )
        for key in checklist_concursos.keys():
            search_in_dump(html, key, constant.CHECKLIST_CONCURSO_SEARCH[key])
            

def explain():
   print("\n")
   for key in checklist_concursos.keys():
        if checklist_concursos[key]:
           print("Foi encontrada uma referencia a ", key, ":", checklist_concursos[key])
        else: 
           print("Não foi encontrada nenhuma referência a", key)
   print("\n")



def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    possible_urls = []
    for elem in html.find_all(href=True):
        for s in constant.CONCURSO_PUBLICO: 
            if s in elem.getText():
                possible_urls.append(elem['href'])
    

    validate_items(elem['href'])
    explain()

main()
