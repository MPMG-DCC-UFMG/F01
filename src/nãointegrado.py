import codecs
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

file = codecs.open('/home/asafe/GitHub/Coleta_F01/governador_valadares/prefeitura/data/raw_pages/56e49a4e6f2a8456f80c0efc03acd703.html', 'r', 'latin-1')
try:
    markup = BeautifulSoup(file.read(),  "html.parser" )
except TypeError:
    print('deu erro')



#Informações-------------------- Link de respostas a perguntas mais frequentes da sociedade.----------------------------

# def search_keywords_faq(markup, constants):
#     questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
#     for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
#         questions_by_t.add(a.getText())
#     return markup.find(text=constants), questions_by_t

# def predict_faq(search_term, keywords, path_base, num_matches = 1,
#     job_name = 'index_gv', threshold= 0):

#     sorted_result = indexing.request_search(
#       search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
#     path = [i[2] for i in sorted_result]
#     path_html = path_functions.agg_paths_by_type(path)["html"]

#     ans = {
#         'page': None,
#         'title': None,
#         'questions': None,
#         'classifier': None 
#     }

#     for filename in path_html:
#         try:
#             markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
#             title, questions = search_keywords_faq(markup, constant.FAQ_SEARCH)
#             classifier = title is not None and questions is not None
#             if title is not None and questions is not None:
#                 ans = {
#                     'page': filename,
#                     'title': title,
#                     'questions': questions
#                 }
#                 return True, ans
#         except TypeError:
#             continue
#     return False, ans


# def explain_faq(isvalid, faq_dict):
#     print("PREDICTION Perguntas Frequentes:", isvalid) 
#     if isvalid :  
#         print(f"Na página direcionada {faq_dict['page']} foi encontrado o seguinte título:", faq_dict['title'])    
#         print("Foram encontradas", len(faq_dict['questions']), "perguntas na página\n")
#         for q in faq_dict['questions']:
#             print(q)

#     elif isvalid is False:     
#         print("\nNenhuma das palavras chave a seguir foram encontradas na página direcionada pelo indexador:")
#         for fs in constant.FAQ_SEARCH:
#             print(fs, ' ')