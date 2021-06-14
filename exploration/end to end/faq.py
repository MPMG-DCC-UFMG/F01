from bs4 import BeautifulSoup
import pandas as pd
import codecs
import re
import constant
from os import walk

#Tag item exists
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.FAQ, href=True)

def predict(markup):
    questions = markup.find_all(text= re.compile(r'[?]+$'))
    return markup.find(text=constant.FAQ_SEARCH), questions

def explain(ans, macro, questions):
    if(ans is not None):
        print("Foi encontrado no menu principal do portal um link que tinha como valor textual:", macro.getText())
        print("Na página direcionada pelo link foi encontrado o seguinte título:", ans)
        print("Foram encontradas", len(questions), "questões na página")

def main():
    macro = get_macro()
    if(not macro):  return 

    filename = './Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
    ans, questions = predict(markup)
    print(ans is not None and questions is not None)
    explain(ans, macro, questions)

main()