from bs4 import BeautifulSoup
import codecs
import re
import constant
from os import walk

def search_keywords_faq(markup, constants):
    questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
     
    for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
        questions_by_t.add(a.getText())
    return markup.find(text=constants), questions_by_t

def predict_faq():
    filename = '../../Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
    title, questions = search_keywords_faq(markup, constant.FAQ_SEARCH)
    classifier = title is not None and questions is not None

    print("\nPrediction FAQ:", classifier)
    ans = {
        'title': title,
        'questions': questions,
        'classifier': classifier 
    }

    return ans

def explain_faq(faq_dict):
    if(faq_dict['classifier']):    
        
        print("\nNa página direcionada pelo link foi encontrado o seguinte título:", faq_dict['title'])    
        print("Foram encontradas", len(faq_dict['questions']), "perguntas na página\n")
        for q in faq_dict['questions']:
            print(q)
        
    elif faq_dict['title'] is None:
               
        print("\nNenhuma das palavras chave a seguir foram encontradas na página direcionada pelo link:")
        for fs in constant.FAQ_SEARCH:
            print(fs, ' ')
        

