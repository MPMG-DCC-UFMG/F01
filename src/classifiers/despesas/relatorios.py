from utils import indexing
from utils import check_df
from utils import path_functions
import pandas as pd
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
    # pdf_files = indexing.get_files_to_valid(
    #     search_term, keywords, num_matches,
    #     job_name, path_base, 'pdf')

    # html_files = path_functions.filter_paths2(html_files, filter_words)
    # pdf_files = path_functions.filter_paths2(pdf_files, filter_words)
    if verbose:
        print('\nPredict Plano Plurianual:')
        print(html_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)
    # result_pdf = analyze_pdf (path_base, pdf_files, keyword_to_search=keywords, page_limit=4, verbose=verbose)
    # df = pd.concat([result, result_pdf])

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result

# Link de acesso à Lei de Diretrizes Orçamentarias do município
def predict_lei_diretrizes_orcamentarias(search_term = 'Diretrizes orçamentárias LDO',
    keywords=['Diretrizes orçamentárias', 'metas fiscais', 'lei diretrizes orçamentárias', 'LDO'],
    filter_words=['despesas', 'orçamento', 'LDO', 'leis_orcamentarias'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, filter_words)

    if verbose:
        print('\nPredict Lei de Diretrizes Orçamentaria:')
        print(html_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result
    
# Link de acesso à Lei Orçamentária Anual do município
def predict_lei_orcamentaria_anual(search_term = 'Lei orçamentária anual LOA',
    keywords=['LOA', 'LOA Lei', 'Lei orçamentária anual', 'orçamentária anual'],
    filter_words=['despesas', 'orçamento', 'LOA', 'leis_orcamentarias'] , path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, filter_words)

    if verbose:
        print('\nPredict Lei Orçamentária Anual:')
        print(html_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result


# Apresentação do balanço anual, com as respectivas demonstrações contábeis
def predict_balanco_demonstracoes(search_term = 'Balanço anual Demonstrações Contábeis',
    keywords=['Balanço anual', 'Demonstrações Contábeis', 'Balancete da Despesa', 'Balanço Orçamentário de Despesas', ' Balanço Patrimonial'],
    filter_words=['despesas', 'orçamento', 'balanço', 'prestacao_de_contas', 'relatorios_de_gestao_fiscal', 'contas_publicas'],
    path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, filter_words)

    if verbose:
        print('\nPredict Balanço anual e demonstrações contábeis:')
        print(html_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    return isvalid, result

# Relatórios da execução orçamentária e gestão fiscal
def predict_execucao_orcamentaria_gestao_fiscal(search_term = 'Relatórios execução orçamentária gestão fiscal',
    keywords=['execução orçamentária', 'gestão fiscal', 'execução orçamentaria', 'prestacao_de_contas', 'relatorios de gestao fiscal'],
    filter_words=['despesas', 'orçamento', 'balanço', 'prestacao_de_contas', 'relatorios_de_gestao_fiscal', 'contas_publicas'],
    path_base='/home', num_matches = 300, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, filter_words)

    if verbose:
        print('\nPredict Relatórios da execução orçamentária e gestão fiscal:')
        print(html_files)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=keywords)

    #Check result 
    isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
    print(result)
    return isvalid, result

def explain(isvalid, df_result, column_name, elemento, verbose=False):

    result = f"Explain - Quantidade de entradas analizadas: {len(df_result[column_name])}. Quantidade de entradas que possuem referência ao item '{elemento}' válido: {sum(df_result[column_name] > 0)}"""

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result



