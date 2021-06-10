from bs4 import BeautifulSoup
import pandas as pd
import codecs
import constant
from os import walk

#Tag item exists
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.FAQ, href=True)['href']

def validate_item(markup):
    return markup.find(text=constant.FAQ_SEARCH) is not None

def main():
    macro = get_macro()
    if(not macro):  return 

    filename = './Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )

    print(validate_item(markup))

main()