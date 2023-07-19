import utilconst.constant as constant
from src.validadores.utils import indexing
from src.validadores.utils import check_df
from src.validadores.utils.analyze_pdf import remove_noise
from src.validadores.utils.analyze_pdf import count_matches
from src.validadores.utils.analyze_pdf import pdf_from_image
from src.validadores.utils.analyze_pdf import pdf_to_text
from src.validadores.utils.analyze_pdf import analyze_pdf

from src.validadores.utils.search_html import analyze_html
import pandas as pd

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

    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)
    pdf_files = filter(lambda filename: filter_word in filename, pdf_files)
    pdf_files = list(pdf_files)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['total', 'totais', 'recebidos'])
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=['atendidos', 'solucionado', 'concedidos'], verbose=False)
    df_atendidos = pd.concat([result, result_pdf])
    #Check result 
    isvalid = check_df.files_isvalid(df_atendidos, column_name='matches', threshold=0)
    return isvalid, result


# Quantidade e/ou percentual de pedidos atendidos
def predict_pedidos_atendidos(search_term = 'Pedidos de acesso informa',
    keywords=['Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)
    pdf_files = filter(lambda filename: filter_word in filename, pdf_files)
    pdf_files = list(pdf_files)

    # print("html_filess:")
    # for file in html_files:
    #     print (file)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['atendidos', 'solucionado', 'concedidos'])
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=['atendidos', 'solucionado', 'concedidos'], verbose=False)
    df_atendidos = pd.concat([result, result_pdf])
    #Check result 
    isvalid = check_df.files_isvalid(df_atendidos, column_name='matches', threshold=0)
    return isvalid, result


# Quantidade e/ou percentual de pedidos indeferidos	
def predict_pedidos_indeferidos(search_term = 'Pedidos de acesso informa',
    keywords=['Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],  
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)
    pdf_files = filter(lambda filename: filter_word in filename, pdf_files)
    pdf_files = list(pdf_files)

    #Analyze all html files searching keywords
    result = analyze_html(html_files, keyword_to_search=['indeferidos', 'negados'])
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=['atendidos', 'solucionado', 'concedidos'], verbose=False)
    df_atendidos = pd.concat([result, result_pdf])
    #Check result 
    isvalid = check_df.files_isvalid(df_atendidos, column_name='matches', threshold=0)
    return isvalid, result

def predict_relatorio_estatistico(search_term = 'Pedidos de acesso informa atendimentos',
    keywords=['atendimentos', 'Pedidos de', 'total', 'no prazo', 'em atraso', 'prorrogados', 'indeferidos', 'concedidos'],
    filter_word='esic' , path_base='/home', num_matches = 100, job_name = ''):

    keywords_recebidos = ['total', 'totais', 'recebidos']
    keywords_atendidos = ['atendidos', 'solucionado', 'concedidos']
    keywords_indeferidos = ['indeferidos','negados']

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = filter(lambda filename: filter_word in filename, html_files)
    html_files = list(html_files)

    pdf_files = filter(lambda filename: filter_word in filename, pdf_files)
    pdf_files = list(pdf_files)

    #Analyze all html files searching keywords
    result_html_recebidos = analyze_html(html_files, keywords_recebidos)
    result_html_atendidos = analyze_html(html_files, keywords_atendidos)
    result_html_indeferidos = analyze_html(html_files, keywords_indeferidos)

    matches_recebidos = []
    matches_atendidos = []
    matches_indeferidos = []

    # PDF
    for file in pdf_files:
        print("aux:", file, "***********")
        content = pdf_to_text(file, fixed_file="", path=path_base, drawing=True, verbose=False)
        content = remove_noise(content)
        # print(path_functions.get_url("/home/asafe", path), count_matches (text, keywords))

        num_matches_recebidos =  count_matches (content, keywords_recebidos)
        num_matches_atendidos = count_matches (content, keywords_atendidos)
        num_matches_indeferidos = count_matches (content, keywords_indeferidos)

        # In case you have not found the keywords, we will do the search with OCR
        if (num_matches_recebidos == 0 or num_matches_atendidos == 0 or num_matches_indeferidos ==0 ):
            content = pdf_from_image(file, verbose=False)
            num_matches_recebidos = count_matches (content, keywords_recebidos)
            num_matches_atendidos = count_matches (content, keywords_atendidos)
            num_matches_indeferidos = count_matches (content, keywords_indeferidos)

        matches_recebidos.append(num_matches_recebidos)
        matches_atendidos.append(num_matches_atendidos)
        matches_indeferidos.append(num_matches_indeferidos)
    
    result_pdf_recebidos = pd.DataFrame({'files': pdf_files, 'matches': matches_recebidos})
    result_pdf_atendidos = pd.DataFrame({'files': pdf_files, 'matches': matches_atendidos})
    result_pdf_indeferidos = pd.DataFrame({'files': pdf_files, 'matches': matches_indeferidos})

    df_recebidos = pd.concat([result_pdf_recebidos, result_html_recebidos])
    df_atendidos = pd.concat([result_pdf_atendidos, result_html_atendidos])
    df_indeferidos = pd.concat([result_pdf_indeferidos, result_html_indeferidos])

    #Check result 
    isvalid_recebidos = check_df.files_isvalid(df_recebidos, column_name='matches', threshold=0)
    isvalid_atendidos = check_df.files_isvalid(df_atendidos, column_name='matches', threshold=0)
    isvalid_indeferidos = check_df.files_isvalid(df_indeferidos, column_name='matches', threshold=0)

    return (isvalid_recebidos, df_recebidos), (isvalid_atendidos,df_atendidos), (isvalid_indeferidos,df_indeferidos)

def explain(df, column_name, elemento, verbose=False):

    result = "Explain - Quantidade de arquivos analizados: {} . Quantidade de aquivos que possuem o item '{}': {}".format(
        len(df[column_name]), elemento, sum(df[column_name] > 0))

    if verbose:
        print(result)

    return result