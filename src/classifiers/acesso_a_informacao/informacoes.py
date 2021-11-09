from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import codecs
import re
from classifiers import constant
from os import walk
import pandas as pd
from utils import indexing
from utils import path_functions
from utils import read
from utils import check_df


def count_matches (text, keyword_to_search):

    matches = 0
    for i in keyword_to_search:
        matches += text.count(i)
    if (matches):
        return 1
    else: return 0

def analyze_html(html_files, keyword_to_search):

    matches = []

    for path in html_files:
        
        text = read.read_file(path)
        # print(path_functions.get_url("/home/asafe", path), count_matches (text, keyword_to_search))
        matches.append(count_matches (text, keyword_to_search))

    result = pd.DataFrame({'files': html_files, 'matches': matches})

    return result

#--------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------Sub_tags Informações ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

# Aba denominada “Transparência” no menu principal
def search_keywords_linkportal(markup, constants):
    macro = markup.findAll(href = re.compile(f"{constants}")) 
    return macro

def predict_link_portal(search_term = 'Prefeitura', 
    keywords = ['Home', 'Menu', 'Transparência', 'Portal'],
    path_base ="/home", num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = filter(lambda filename: 'prefeitura' in filename and 'mg.gov.br' in path_functions.get_url(path_base, filename), html_files)
    html_files = list(html_files)


    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search = constant.ABA_TRANSPARENCIA[job_name])

    n_files = len(result.index)

    #Check result 
    isvalid = check_df.infos_isvalid(result, column_name='matches', threshold = n_files/2)

    return isvalid, result

def explain_link_portal(df, column_name, elemento, verbose=False):

    result = "Explain - Quantidade de arquivos analizados: {} . Quantidade de aquivos que possuem o item '{}': {}".format(
        len(df[column_name]), elemento, sum(df[column_name]))

    if verbose:
        print(result)

    return result


# Texto padrão explicativo sobre a Lei de Acesso à Informação -------------------------------------

def search_keywords_text_expl(df, markup, constants):
    # buscar pelo indexador por arquivos que contenham: constants.LEI_ACESSO_INFORMACAO e verificar se este contem
    # LEI_ACESSO_INFORMACAO_CONTEUDO
    markup = markup.get_text()

    page_results = []

    for macro in constants:
        # print(macro)

        try:
            if re.search(f'.*{macro}.*', markup, re.IGNORECASE) != None:
                page_results.append(1)
            else: 
                page_results.append(0)

        except TypeError:
            page_results.append(0)

    return page_results

def predict_text_expl(search_term = 'Lei', keywords=['LAI', 'Lei de acesso à informação'], 
    path_base='/home', num_matches = 60, job_name = ''):

    paths_html = indexing.get_files_to_valid( search_term, keywords, num_matches, job_name, path_base)

    columns = constant.LEI_ACESSO_INFORMACAO_CONTEUDO
    result = pd.DataFrame( columns=columns, index=paths_html)

    # print(path_html)

    for index, item in enumerate(paths_html, start=0):
        # print('result[index]', item, '\n', path_functions.get_url(path_base, item))
        markup = read.read_html(item)

        page_results = search_keywords_text_expl(result, markup, constant.LEI_ACESSO_INFORMACAO_CONTEUDO)

        # print(path_functions.get_url(path_base, item), page_results)
        result.loc[item] = page_results

    result['sum'] = result.iloc[:,:].sum(axis=1)

    # Verificar se algum dos resultados apresentou mais que duas  das keywords 
    if (len(result[result['sum'] > 1]) > 0):
        return True, result
    else:
        return False, result

def new_predict_text_expl(search_term = 'Lei', keywords=['LAI', 'Lei de acesso à informação', "Lei Federal 12.527"],  
    path_base='/home', num_matches = 60, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=constant.LEI_ACESSO_INFORMACAO_CONTEUDO)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    return isvalid, result

def explain_text_expl(isvalid, result):

    print(result.index, result['sum'])
    if (isvalid):
        result_explain = (f"Texto padrão explicativo sobre a Lei de Acesso à Informação foi encotrado, de {len(result)} documentos candidados {len(result[result['sum'] > 2])} deles tem pelo menos 2 das keywords")
    else:
        result_explain = (f"Texto padrão explicativo sobre a Lei de Acesso à Informação não foi encotrado, de {len(result)} documentos candidados nenhum deles tem pelo menos 2 das keywords \n")
    return result_explain

# Link de acesso à leg federal sobre a transp (Lei nº 12.527/2011) ----------------------------------

def search_keywords_legs_federal(markup, constants):
    target = []
    for a in markup.findAll(href = re.compile(constants, re.IGNORECASE)):
        target.append(a)
    target = set(target)
    # print(target)
    return target

def predict_legs_federal(search_term='Acesso a informao', keywords=['http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm'], 
    path_base = '/home', num_matches = 40, job_name = ''):

    paths_html = indexing.get_files_to_valid( search_term, keywords, num_matches, job_name, path_base)

    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in paths_html:
        # print(path_functions.get_url(path_base, filename), filename)
        markup = read.read_html(filename)
        result['macro'] = search_keywords_legs_federal(markup,constant.LINK_LEGS_FEDERAL)

        if len(result['macro']):
            result['file_name'] = filename
            result['url'] = path_functions.get_url(path_base, filename)

            return True, result
            
    return False,None

def explain_legs_federal(isvalid, result):
    if isvalid:
        result_explain = f" O link foi encontrado em {result['url']}"
    else:
        result_explain = " O link da lei 12.527 não foi encontrado."
    return result_explain
     
# Link de acesso à leg Estadual sobre a transparência (Decreto Estadual nº 45.969/2012)-----------------
def search_keywords_legs_estadual(markup, constants):
    target = []
    for a in markup.findAll(href = re.compile(constants, re.IGNORECASE)):
        target.append(a)
    return target
    
def predict_legs_estadual(search_term='Acesso a informao', keywords=['https://www.almg.gov.br/consulte/legislacao/completa/completa.html?num=45969&ano=2012&tipo=DEC'],
    path_base = '/home', num_matches = 40, job_name = ''):

    paths_html = indexing.get_files_to_valid( search_term, keywords, num_matches, job_name, path_base)

    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in paths_html:
        # print(filename)
        markup = read.read_html(filename)
        result['macro'] = search_keywords_legs_estadual(markup,constant.LINK_LEGS_ESTADUAL)

        if len(result['macro']):
            result['file_name'] = filename
            result['url'] = path_functions.get_url(path_base, filename)
            return True, result
            
    return False,None

def explain_legs_estadual(isvalid, result):
    if isvalid:
        result_explain = (f"\tO link foi encontrado em [{result['file_name']}, {result['url']} ] no(s) elemento(s): {result['macro']}")
    else:
        result_explain = ("\tO link do Decreto Estadual nº 45.969/2012 não foi encontrado.")
    return result_explain


# Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)

def search_keywords_site_transparencia(markup, constants):
    target = []
    for a in markup.findAll(href = constants):
        target.append(a)
    return target

def predict_site_transparencia(search_term='Acesso a informao', keywords=['www.transparencia.mg.gov.br'], 
    path_base='/home', num_matches = 40, job_name = ''):

    paths_html = indexing.get_files_to_valid( search_term, keywords, num_matches, job_name, path_base)

    results = []
    result = {
        'file_name' : None,
        'url': None,
        'macro': None,
    } 

    for filename in paths_html:
        # print(path_functions.get_url(path_base, filename))
        markup = read.read_html(filename)
        macro = search_keywords_site_transparencia(markup,constant.URL_TRANSPARENCIA_MG)

        if len(macro):
            result['file_name'] = filename
            result['url'] = path_functions.get_url(path_base, filename)
            result['macro'] = macro

            results.append(result)
    if len(results):
        return True, results
    else:
        return False,None

def explain_site_transparencia(isvalid, results):

    if isvalid:
        result_explain = "O link foi encontrado em: "
        links = []
        for result in results:
            links.append(result['url'])
        links = set(links)
        for link in links:
            result_explain += f" {link};"
    else:
        result_explain = f"Não foi encontrado um link para uma das páginas: {constant.URL_TRANSPARENCIA_MG}"
    return result_explain
    
# Acesso ilimitado a todas as informações públicas do sítio eletrônico: o acesso sem cadastro ou ao fornecimento de dados pessoais

def predict_acesso_ilimitado(search_term = 'Login', keywords = ['login', 'necessrio efetuar login', 'clique aqui para fazer login', 'clique aqui para fazer cadastro', 'para baixar necessrio'], 
    path_base = '/home', num_matches = 1000, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search = keywords)

    #Check result 
    isvalid = check_df.infos_isvalid(result, column_name='matches', threshold = 0)

    return not isvalid, result

def explain_acesso_ilimitado(isvalid, df, column_name, elemento):

    if isvalid:
        result = "Não foi encontrada referẽncia a login no portal"
    else:
        result = "Explain - Quantidade de arquivos analizados: {}. Quantidade de aquivos que possuem referência a '{}': {}".format(
            len(df[column_name]), elemento, sum(df[column_name]))

    return result


# Link de respostas a perguntas mais frequentes da sociedade.
def predict_faq(search_term = 'Perguntas Frequentes', 
    keywords = ['FAQ', 'Perguntas Frequentes'], 
    num_matches = 30, job_name = "", path_base = "", verbose = False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print("Predict - Possui referência a Perguntas Frequentes: {}".format(isvalid))

    return isvalid, result

def explain_faq(isvalid, result):

    if isvalid:
        result = f"Explain - Quantidade de aquivos que possuem o item 'Perguntas Frequentes' : {len(result)}"
    else:
        result = "Nenhuma referência a Perguntas Frequentes foi encontrada nas páginas"

    return result


def explain(df, column_name, elemento, verbose=False):

    result = "Explain - Quantidade de arquivos analizados: {} . Quantidade de aquivos que possuem o item '{}': {}".format(
        len(df[column_name]), elemento, sum(df[column_name]))

    if verbose:
        print(result)

    return result

