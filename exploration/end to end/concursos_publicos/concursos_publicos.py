import codecs
import os
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

def convert_url_to_dir(url): #still needs solution
    #return url.replace(constant.URL, '')
    return 'downloads/categoria/ConcursoPublico-EditalNo00120190022019e0032019.html'

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

def search_in_dump(markup, item, search):
    
    for div in markup.find_all('div', {"class": "list-group"}):
        checklist_concursos['registro'] = True #Existe algum registro dos concursos públicos
        link = constant.URL + div.find('a', href = True)['href']
        for s in search:
            if(s in div.find('h4').getText() and validate_file(link)):  
                checklist_concursos[item] = True
                return
        

def validate_items(url):
    dir = convert_url_to_dir(url)
    if os.path.exists('./Governador Valadares/' + dir):
        html = BeautifulSoup(codecs.open('./Governador Valadares/' + dir, 'r', 'utf-8').read(),  "html.parser" )
        for key in checklist_concursos.keys():
            search_in_dump(html, key, constant.CHECKLIST_CONCURSO_SEARCH[key])
            
    print(checklist_concursos)


def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    
    for elem in html.find_all(href=True):
        for s in html: 
            if s in constant.CONCURSO_PUBLICO: 
                if s in elem.getText() and validate_items(elem['href']): return True

main()
