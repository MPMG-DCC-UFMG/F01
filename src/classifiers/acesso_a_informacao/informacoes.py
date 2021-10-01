from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import codecs
import re
import constant
from os import walk
import pandas as pd
from utils import indexing
from utils import table_to_csv
from utils import search_path_in_dump
from lxml import etree
import lxml.html
from lxml.cssselect import CSSSelector
import json


#--------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------Sub_tags Informações ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

#Informações-------- Aba denominada “Transparência” no menu principal
def search_keywords_linkportal(markup, constants):
    macro = markup.findAll(href = constants) 
    return macro

def predict_link_portal(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
        search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)

    # paths = search_path_in_dump.get_paths(sorted_result)
    # paths = (sorted(set(paths)))
    # paths = search_path_in_dump.filter_paths(paths, word="prefeitura")

    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    result = {
    'filename' : None,
    'url': None,
    'LINK_NO_MENU' : False,
    'macro': None,
    'xpath': []
    }

    print(path_html)
    for filename in path_html:

        if 'prefeitura' in filename:
            print('vish',filename,"******")
            result['filename'] = filename

            url = search_path_in_dump.get_url(path_base, filename)
 
            result['url'] = url

            try:
                file = codecs.open(filename, 'r', 'latin-1')
                markup = BeautifulSoup(file.read(),  "html.parser" )
                macro = search_keywords_linkportal(markup,constant.ABA_TRANSPARENCIA[job_name])
                result['macro'] = macro

                # Search xpath
                arquivo = codecs.open(filename, 'r', 'latin-1')
                dom =  lxml.html.fromstring(arquivo.read())
                selAnchor = CSSSelector('a')
                tree = etree.ElementTree(dom)
                foundElements = selAnchor(dom)
                for e in foundElements:
                    if e.get('href') == constant.ABA_TRANSPARENCIA[job_name]:
                        # print(e.get('href'))
                        result['xpath'].append(tree.getpath(e))


                if len(macro) == 0:
                    return False, result
                else:
                    tags_a = macro
                    for tag_a in tags_a:
                        tag_parent = tag_a.parent
                        tag_grandparent = tag_parent.parent
                        if tag_grandparent.find(class_= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*|.*menuprincipal.*)", re.IGNORECASE)):
                            result['LINK_NO_MENU'] = True
                        if tag_grandparent.find(id= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*|.*menuprincipal.*)", re.IGNORECASE)):
                            result['LINK_NO_MENU'] = True

                    return True, result
            except TypeError:
                continue
            
    return False, result


def explain_link_portal(isvalid, result):
    print("PREDICTION Link para Portal no menu:", result['LINK_NO_MENU']) 
    if(isvalid):
        print(f"Link para o portal da transparencia encontrado em {result['filename']}, link: {result['url']}")
        print(f"Link para o portal da transparencia encontrado no site na tag: {result['macro']}")  
        print(f"No(s) seguinte(s) xpath(s): {result['xpath']}")
        if(result['LINK_NO_MENU']):
            print("\t O link provavelmente está no menu")
        else:
            print("\t O link provavelmente não está no menu")
    
    else:
        print("Link para o portal da transparencia não foi encontrado no site")  


#Informações------- Texto padrão explicativo sobre a Lei de Acesso à Informação -------------------------------------

def search_keywords_text_expl(df, markup, constants):
    # buscar pelo indexador por arquivos que contenham: constants.LEI_ACESSO_INFORMACAO e verificar se este contem
    # LEI_ACESSO_INFORMACAO_CONTEUDO
    markup = markup.get_text()

    page_results = []

    for macro in constants:

        try:
            if re.search(f'.*{macro}.*', markup, re.IGNORECASE) != None:
                page_results.append(1)
            else: 
                page_results.append(0)

        except TypeError:
            page_results.append(0)

    return page_results

    
def predict_text_expl(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
        search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)

    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    columns = constant.LEI_ACESSO_INFORMACAO_CONTEUDO

    result = pd.DataFrame( columns=columns, index=path_html)

    for index, item in enumerate(path_html, start=0):
        # print('result[index]', item, '\n', search_path_in_dump.get_url(path_base, item))
        print(search_path_in_dump.get_url(path_base, item))
        file = codecs.open(item, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )

        page_results = search_keywords_text_expl(result, markup, constant.LEI_ACESSO_INFORMACAO_CONTEUDO)
        result.loc[item] = page_results

    result['sum'] = result.iloc[:,:].sum(axis=1)

    # Verificar se algum dos resultados apresentou mais que duas  das keywords 
    if (len(result[result['sum'] > 2]) > 0):
        return True, result
    else:
        return False, result

def explain_text_expl(isvalid, result):

    # print(result)
    print("PREDICTION texto padrão explicativo:", isvalid) 

    if (isvalid):
        print(f"Texto padrão explicativo sobre a Lei de Acesso à Informação foi encotrado")

        print(f"\tDe {len(result)} documentos candidados {len(result[result['sum'] > 2])} deles tem mais de 2 das 6 keywords")
    else:
        print("Texto padrão explicativo sobre a Lei de Acesso à Informação não foi encotrado")
        x = 1
        print(f"\tDe {len(result)} documentos candidados nenhum deles tem mais de 2 das 6 keywords \n")


#Informações----- Link de acesso à leg federal sobre a transp (Lei nº 12.527/2011) ----------------------------------

def search_keywords_legs_federal(markup, constants):
    target = []
    for a in markup.findAll(href = constants):
        target.append(a)
    target = set(target)
    return target

def predict_legs_federal(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in path_html:
        # print(filename)
        file = codecs.open(filename, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )
        result['macro'] = search_keywords_legs_federal(markup,constant.LINK_LEGS_FEDERAL)

        if len(result['macro']):
            result['file_name'] = filename
            result['url'] = search_path_in_dump.get_url(path_base, filename)

            return True, result
            
    return False,None

def explain_legs_federal(isvalid, result):
    print("PREDICTION Link Legislação Federal:", isvalid) 
    if isvalid:
        print(f"\tO link foi encontrado em [{result['file_name']}, {result['url']} ] no(s) elemento(s): {result['macro']}")
    else:
        print("\tO link da lei 12.527 não foi encontrado.")
     

#Informações----- Link de acesso à leg Estadual sobre a transparência (Decreto Estadual nº 45.969/2012)-----------------
def search_keywords_legs_estadual(markup, constants):
    target = []
    for a in markup.findAll(href = constants):
        target.append(a)
    return target
    
def predict_legs_estadual(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in path_html:
        # print(filename)
        file = codecs.open(filename, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )
        result['macro'] = search_keywords_legs_estadual(markup,constant.LINK_LEGS_ESTADUAL)

        if len(result['macro']):
            result['file_name'] = filename
            result['url'] = search_path_in_dump.get_url(path_base, filename)
            return True, result
            
    return False,None

def explain_legs_estadual(isvalid, result):
    print("PREDICTION Link Legislação Estadual:", isvalid) 
    if isvalid:
        print(f"\tO link foi encontrado em [{result['file_name']}, {result['url']} ] no(s) elemento(s): {result['macro']}")
    else:
        print("\tO link do Decreto Estadual nº 45.969/2012 não foi encontrado.")


#Informações------------- Link de acesso ao site da Transparência (www.transparencia.mg.gov.br) ----------------------

def search_keywords_site_transparencia(markup, constants):
    target = []
    for a in markup.findAll(href = constants):
        target.append(a)
    return target

def predict_site_transparencia(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    results = []
    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in path_html:
        # print(search_path_in_dump.get_url(path_base, filename))
        file = codecs.open(filename, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )
        result['macro'] = search_keywords_site_transparencia(markup,constant.URL_TRANSPARENCIA_MG)

        if len(result['macro']):
            result['file_name'] = filename
            result['url'] = search_path_in_dump.get_url(path_base, filename)

            results.append(result)
            # return True, result
    if len(results):
        return True, results
    else:
        return False,None

def explain_site_transparencia(isvalid, results):
    print("PREDICTION Link para site Transparencia:", isvalid) 
    if isvalid:
        print(f"O link foi encontrado em")
        for result in results:
            print(f"\t[{result['file_name']}, {result['url']} ] no(s) elemento(s): {result['macro']}]")
    else:
        print("Não foi encontrado um link para uma das páginas \n", constant.URL_TRANSPARENCIA_MG)
    


#Informações----- Acesso ilimitado a todas as informações públicas do sítio eletrônico: o acesso sem cadastro ou ao fornecimento de dados pessoais

def search_keywords_acesso_ilimitado(markup):
    macro = set(markup.find_all(text = re.compile(r'(login)')))
    # markup = markup.get_text()
    # for expression in constants:
    #     if (re.search(f'.*{expression}.*', markup, re.IGNORECASE)) != None:
    #         macro.add(expression)

    # print(macro)
    return macro

def predict_acesso_ilimitado(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
        search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)

    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    result = []

    for filename in path_html:
        file = codecs.open(filename, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )
        macro = search_keywords_acesso_ilimitado(markup)
        if (len(macro) != 0):
            result.append({'filename': filename, 'url': search_path_in_dump.get_url(path_base, filename), 'macro': macro})

    if (len(result) > 0):
        return False, result

    return True,result

def explain_acesso_ilimitado(isvalid, result):
    print("PREDICTION Acesso Ilimitado:", isvalid) 

    if (isvalid):
        print("Não foi encontrado uma referência a 'login' nas páginas analisadas")
    else:
        print("Nas seguintes páginas foram encontrados elementos com as seguinte referências a login")
        for res in result:
            print(res['filename'] + ', ' + res['url'], ':', res['macro'])
        
    

#Informações-------------------- Link de respostas a perguntas mais frequentes da sociedade.----------------------------

# def search_keywords_faq(markup, constants):
#     questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
#     for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
#         questions_by_t.add(a.getText())
#     return markup.find(text=constants), questions_by_t

# def predict_faq(search_term, keywords, path_base, num_matches = 1,
#     job_name = 'index_gv', threshold= 0):

#     _, sorted_result = indexing.request_search(
#       search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
#     path = [i[2] for i in sorted_result]
#     path_html = search_path_in_dump.agg_type(path)["html"]

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

def search_keywords_faq(markup, constant):
    macro = []
    for elem in constant:
        try:
            aux = list(set(markup.find_all(text = re.compile(f'{(elem)}'))))
            if len(aux) > 0:
                for item in aux:
                    macro.append(item)
        except TypeError:
            continue
    
    # print('macro:', set(macro))
    return set(macro)


def predict_faq(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    _, sorted_result = indexing.request_search(
      search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    path = [i[2] for i in sorted_result]
    path_html = search_path_in_dump.agg_type(path)["html"]

    result = []

    for filename in path_html:
        # print(filename)
        file = codecs.open(filename, 'r', 'utf-8')
        markup = BeautifulSoup(file.read(),  "html.parser" )
        macro = search_keywords_faq(markup, constant.FAQ_SEARCH)
        if (len(macro) != 0):
            result.append({'filename': filename, 'url': search_path_in_dump.get_url(path_base, filename), 'macro': macro})

    if (len(result) > 0):
        return True, result

    return False,result
        

def explain_faq(isvalid, result):
    print("PREDICTION Perguntas Frequentes:", isvalid) 
    if isvalid :  
        print('Nas seguintes páginas foram encontrados elementos com os seguintes textos:')
        for res in result:
            print('Página:', res['filename'] + ', ' + res['url'], '\n\tElemento:', res['macro'])

    elif isvalid is False:     
        print("\nNenhuma das palavras chave a seguir foram encontradas nas páginas direcionadas pelo indexador:")
        for fs in constant.FAQ_SEARCH:
            print(fs, ' ')

def predict_informacoes():

    print("\n -------------- PREDICTION Informação:  ------------------- \n")

    # link_portal_dict = predict_link_portal()

    # text_expl_dict = predict_text_expl()

    legs_federal_dict = predict_legs_federal()

    # legs_estadual_dict = predict_legs_estadual()

    # site_transparencia_dict =  predict_site_transparencia()

    # acesso_ilimitado_dict = predict_acesso_ilimitado()

    # faq_dict = predict_faq()


    # informacoes_dict = { 'link_portal_dict': link_portal_dict, 
    #                     'faq_dict': faq_dict ,
    #                     'site_transparencia_dict' : site_transparencia_dict,
    #                     }

    # return informacoes_dict
    return legs_federal_dict


def explain_informacoes(informacoes_dict):

    print("\n ------------------ Explain Informação:  ---------------")


    print("\n - Explain Informação: Aba denominada transparencia no menu principal: - \n")
    link_portal_dict = informacoes_dict['link_portal_dict']
    explain_link_portal(link_portal_dict)

    print("\n - Explain Informação: Perguntas Frequentes: - \n")
    faq_dict = informacoes_dict['faq_dict']
    explain_faq(faq_dict)

    print("\n - Explain Informação: Link de acesso ao site da Transparência (www.transparencia.mg.gov.br): - \n")
    site_transparencia_dict = informacoes_dict['site_transparencia_dict']
    explain_site_transparencia(site_transparencia_dict)

    print("\n\n")