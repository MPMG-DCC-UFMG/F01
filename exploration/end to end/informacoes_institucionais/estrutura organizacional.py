import codecs
import os
import sys
import requests
import constant
from bs4 import BeautifulSoup

def explain(title, url):
    if(title):
        if (constant.URL not in url): url = constant.URL + url
        print("Na home do portal foi encontrado um link com o seguinte valor textual:", title)
        print("O link", url, "é válido")
    else: 
        print("Não foi encontrada nenhuma das seguintes palavras chave com links validos:")
        for w in constant.ORGANITAZION:
            print(w)

def validate_checklist_item(url):
    dir = url.replace(constant.URL, '')
    if os.path.exists('./Governador Valadares/' + dir):
        return True
    try:
        if (constant.URL not in url): url = constant.URL + url
        request = requests.get(url)
        print('Trying to reach ', url)
        if request.status_code < 400:  return True

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, TimeoutError):
        print("Failed to connect to ", url)

def predict(markup, search):

    for elem in markup.find_all(href=True):
        for s in search: 
            if s in elem.getText() and validate_checklist_item(elem['href']): 
                explain(s, elem['href'])
                return True
    explain(None, None)
    return False
       

def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    print(predict(html, constant.ORGANIZACAO))

main()
