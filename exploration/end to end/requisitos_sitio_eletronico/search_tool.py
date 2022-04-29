import codecs
import utilconst.constant as constant
from bs4 import BeautifulSoup
import re

search_tool = {
    'value': False 
}

def explain():
    if search_tool: print("Foi encontrado um 'input' do tipo texto com algum dos seus atributos com um dos radicais: 'busc', 'pesquis'. Ou a palavra 'search'")
    else: print ("Não foi encontrado um 'input' do tipo texto com algum dos seus atributos com um dos radicais: 'busc', 'pesquis'. Ou a palavra 'search'")
def predict_search_tool(markup):

    search = constant.SEARCH_TOOL

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
 
    for s in search["value"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def validade_atribute_id(elem, search):

    for s in search["value"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def validade_atribute_class(elem, search):

    for s in search["value"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True

def validade_atribute_value(elem, search):

    for s in search["value"]: 
        p = re.compile(f'.*{s}.*')
        if p.match(elem): return True


def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )

    predict = predict_search_tool(html)
    print("Predict: ",predict, "\n")

    explain()

main()