from bs4 import BeautifulSoup
import pandas as pd
import codecs
import re
import utilconst.constant as constant
from os import walk

#Tag item exists
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.FAQ, href=True)

def get_title_and_questions(markup):
    questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
     
    for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
        questions_by_t.add(a.getText())
    return markup.find(text=constant.FAQ_SEARCH), questions_by_t

def predict(title, questions):
    prediction = (title is not None and questions is not None)    
    return prediction

def explain(macro, title, questions):
    if(macro is None):
        print("Não foi encontrado no menu principal do portal um link que possua como valor textual alguma das seguintes palavras chave:")
        for fs in constant.FAQ:
            print(fs, ' ')
        return  
    
    print("Foi encontrado no menu principal do portal um link que tinha como valor textual:", macro.getText(), "\nLink:", macro['href'])
    if(title is None):    
        print("\nNenhuma das palavras chave a seguir foram encontradas na página direcionada pelo link:")
        for fs in constant.FAQ_SEARCH:
            print(fs, ' ')
        return 

    print("\nNa página direcionada pelo link foi encontrado o seguinte título:", title)    
    print("Foram encontradas", len(questions), "perguntas na página\n")

def main():
    macro = get_macro()
    title = None
    questions = None
    if(not macro):  
        prediction = False
    else: 
        filename = './Governador Valadares/faq/perguntas_frequentes.html'
        markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
        title, questions = get_title_and_questions(markup)
        prediction = predict(title, questions)
    
    print("\nPrediction:", prediction, "\n")

    explain(macro, title, questions)

main()