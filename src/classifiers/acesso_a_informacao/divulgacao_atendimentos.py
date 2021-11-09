import constant
from utils import indexing
from utils import check_df
from utils import path_functions
from utils import read
from utils.search_html import analyze_html

#--------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------Relatório estatístico (Divulgação de relatório de atendimentos)------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

# Quantidade de pedidos recebidos
def predict_pedidos_recebidos(search_term = 'Pedidos de acesso informa',
    keywords=['Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    doc_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')


    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)
    doc_files = filter(lambda filename: filter_word in filename, doc_files)
    doc_files = list(doc_files)

    print("html_files:")
    for file in doc_files:
        print (file)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['total', 'totais'])
    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result


# Quantidade e/ou percentual de pedidos atendidos
def predict_pedidos_atendidos(search_term = 'Pedidos de acesso informa',
    keywords=['Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)

    # print("html_filess:")
    # for file in html_files:
    #     print (file)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['atendidos'])
    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result


# Quantidade e/ou percentual de pedidos indeferidos	
def predict_pedidos_indeferidos(search_term = 'Pedidos de acesso informa',
    keywords=['Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],  
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['indeferidos'])
    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result


def explain(df, column_name, elemento, verbose=False):

    result = "Explain - Quantidade de arquivos analizados: {} . Quantidade de aquivos que possuem o item '{}': {}".format(
        len(df[column_name]), elemento, sum(df[column_name] > 0))

    if verbose:
        print(result)

    return result