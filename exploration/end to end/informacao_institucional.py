import codecs
import os
import requests
import constant
from bs4 import BeautifulSoup

def validate_item(url):
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

def search_checklist_item(markup, search):

    for elem in markup.find_all(href=True):
        for s in search: 
            if s in elem.getText() and validate_item(elem['href']): return True

    return False
       

def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    print(search_checklist_item(html, constant.ORGANIZACAO))
    print(search_checklist_item(html, constant.LEGISLACAO_MUNICIPAL))

main()
