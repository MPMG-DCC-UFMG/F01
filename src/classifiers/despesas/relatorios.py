from utils import indexing
import pandas as pd
import sys
from utils import checker
from utils import check_df
from utils import path_functions
import pandas as pd
import numpy as np
from utils.analyze_pdf import analyze_pdf
from utils.search_html import analyze_html

# Link de acesso ao Plano Plurianual do município
def predict_plano_plurianual(search_term = 'Plano Plurianual PPA',
    keywords=['PPA', 'Plano Plurianual', 'PPA Lei'],
    filter_words=['despesas','orçamento','plano_plurianual','PPA','leis_orcamentarias'], 
    path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = path_functions.filter_paths2(html_files, filter_words)
    pdf_files = path_functions.filter_paths2(pdf_files, filter_words)
    if verbose:
        print('\nPredict Descrição:')
        print(html_files, pdf_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    df = pd.concat([result, result_pdf])

    #Check result 
    isvalid = check_df.files_isvalid(df, column_name='matches', threshold=0)
    return isvalid, df

# Link de acesso à Lei de Diretrizes Orçamentarias do município
def predict_lei_diretrizes_orcamentarias(search_term = 'Diretrizes orçamentárias LDO',
    keywords=['Diretrizes orçamentárias', 'metas fiscais', 'lei diretrizes orçamentárias', 'LDO'],
    filter_words=['despesas', 'orçamento', 'LDO', 'leis_orcamentarias'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = path_functions.filter_paths2(html_files, filter_words)
    pdf_files = path_functions.filter_paths2(pdf_files, filter_words)

    if verbose:
        print('\nPredict Descrição:')
        print(html_files, pdf_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    df = pd.concat([result, result_pdf])

    #Check result 
    isvalid = check_df.files_isvalid(df, column_name='matches', threshold=0)
    return isvalid, df
    
# Link de acesso à Lei Orçamentária Anual do município
def predict_lei_orcamentaria_anual(search_term = 'Lei orçamentária anual LOA',
    keywords=['LOA', 'LOA Lei', 'Lei orçamentária anual', 'orçamentária anual'],
    filter_words=['despesas', 'orçamento', 'LOA', 'leis_orcamentarias'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    html_files = path_functions.filter_paths2(html_files, filter_words)
    pdf_files = path_functions.filter_paths2(pdf_files, filter_words)

    if verbose:
        print('\nPredict Descrição:')
        print(html_files, pdf_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    df = pd.concat([result, result_pdf])

    print(df)
    #Check result 
    isvalid = check_df.files_isvalid(df, column_name='matches', threshold=0)
    return isvalid, df


# Apresentação do balanço anual, com as respectivas demonstrações contábeis
def predict_balanco_demonstracoes(search_term = 'Balanço anual Demonstrações Contábeis',
    keywords=['Balanço anual', 'Demonstrações Contábeis'],
    filter_words=['despesas', 'orçamento', 'balanço', 'leis_orcamentarias'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    # html_files = path_functions.filter_paths2(html_files, filter_words)
    # pdf_files = path_functions.filter_paths2(pdf_files, filter_words)

    if verbose:
        print('\nPredict Descrição:')
        print(html_files, pdf_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    df = pd.concat([result, result_pdf])

    print(df)
    #Check result 
    isvalid = check_df.files_isvalid(df, column_name='matches', threshold=0)
    return isvalid, df

# Relatórios da execução orçamentária e gestão fiscal
def predict_balanco_demonstracoes(search_term = 'Relatórios execução orçamentária gestão fiscal',
    keywords=['relatório da execução orçamentária', 'relatório da gestão fiscal', 'relatório de execução orçamentária'],
    filter_words=['despesas', 'orçamento', 'plano_plurianual', 'LOA'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)
    pdf_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base, 'pdf')

    # html_files = path_functions.filter_paths2(html_files, filter_words)
    # pdf_files = path_functions.filter_paths2(pdf_files, filter_words)

    if verbose:
        print('\nPredict Descrição:')
        print(html_files, pdf_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    df = pd.concat([result, result_pdf])

    print(df)
    #Check result 
    isvalid = check_df.files_isvalid(df, column_name='matches', threshold=0)
    return isvalid, df

def explain(isvalid, df_result, column_name, elemento, verbose=False):

    result = f"Explain - Quantidade de entradas analizadas: {len(df_result[column_name])}. Quantidade de entradas que possuem o item '{elemento}' válido: {sum(df_result[column_name] > 0)}"""

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result



