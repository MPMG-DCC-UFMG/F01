import codecs
import constant
from bs4 import BeautifulSoup
import re

def search_checklist_item(markup, search):

    # Search for all inputs none hidden
    for elem in markup.find_all("input", attrs={"type": "text"}):

        # Analyzing input attributes
        try:
            if validade_atribute_name(elem.attrs['name'].lower(), search): return True
        except KeyError:
            pass
        try:
            if validade_atribute_id(elem.attrs['id'].lower(), search): return True
        except KeyError:
            pass
        try:
            if validade_atribute_class(elem.attrs['class'].lower(), search): return True
        except KeyError:
            pass
        try:  
            if validade_atribute_value(elem.attrs['value'].lower(), search): return True
        except KeyError:
            pass

    return False
       
def validade_atribute_name(elem, search):
 
    for s in search["name"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def validade_atribute_id(elem, search):

    for s in search["id"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def validade_atribute_class(elem, search):

    for s in search["class"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True
 

def validade_atribute_value(elem, search):

    for s in search["value"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    print(search_checklist_item(html, constant.SEARCH_TOOL))

main()