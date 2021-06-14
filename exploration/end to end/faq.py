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
    questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
     
    for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
        questions_by_t.add(a.getText())
    return markup.find(text=constant.FAQ_SEARCH), questions_by_t

def explain(ans, macro, questions):
    if(ans is not None):
        print("Foi encontrado no menu principal do portal um link que tinha como valor textual:", macro.getText(), "\nLink:", macro['href'])
        print("\nNa página direcionada pelo link foi encontrado o seguinte título:", ans)
        print("Foram encontradas", len(questions), "perguntas na página\n")

def main():
    macro = get_macro()
    if(not macro):  return 

    filename = './Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
    ans, questions = predict(markup)
    prediction = (ans is not None and questions is not None)
    print("\nPrediction:", prediction, "\n")
    explain(ans, macro, questions)

main()