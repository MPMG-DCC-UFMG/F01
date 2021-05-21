import codecs
import os
import requests
import constant
from os import walk
from bs4 import BeautifulSoup

checklist_viagens = {
    'publicacao_informacoes': False,
    'nome':False,
    'cargo':False,
    'destino':False,
    'atividade':False,
    'periodo':False,
    'num_diarias':False,
    'valor_total':False,
    'base_legal':False
}
#Transforms url extracted in html to dir where the respective html of the link page is
def convert_url_to_dir(url): #still needs solution
    #return url.replace(constant.URL, '')
    return 'despesas-por-diarias/'

def validate_item(headers, key, search):
    for s in search: 
        if next((header for header in headers if s in header.getText()), None): 
            checklist_viagens[key] = True

#Search for checklist atributes in correct page  
def search_in_dump(markup):
    headers = markup.find('thead').find_all('th')
    if markup.find('tbody').find_all('tr'): #if theres any rows in table
        for key in checklist_viagens.keys():
            validate_item(headers, key, constant.CHECKLIST_VIAGEM_SEARCH[key])


#Returns all files that correspond to checklist item       
def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

#iterates through files 
def validate_items(url):
    dir = './Governador Valadares/' + convert_url_to_dir(url)
    if os.path.exists(dir):
        filenames = get_all_filenames_in_dir(dir)
        html = BeautifulSoup(codecs.open('./Governador Valadares/' + dir + filenames[0], 'r', 'utf-8').read(),  "html.parser" )
        search_in_dump(html)    

def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    for elem in html.find_all(href=True):
        for s in constant.DIARIA_VIAGEM: 
            if s in elem.getText() and validate_items(elem['href']): return True

    print(checklist_viagens)
main()