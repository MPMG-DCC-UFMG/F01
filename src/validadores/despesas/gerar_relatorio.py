
from utils import path_functions
from utils import indexing
from utils import check_df
from utils.search_html import analyze_html

# Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto	

def predict_relatorio(search_term = 'Empenhos Pagamentos',
    keywords=['Pagamentos', 'Empenhos'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 100, job_name = '', verbose=False):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths(html_files, filter_words)

    # Analyze 
    result = analyze_html(html_files, keyword_to_search=['pdf', 'excel', 'exportar'], need_one=keywords)

    #Check result 
    isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print('\nPredict gerar relatório da consulta:', isvalid)
    
    return isvalid, result

def explain(isvalid, result, column_name, elemento, verbose=False):

    print(isvalid)
    result = "Explain - {}. Para {} entradas analizadas {} vezes algumas das palavras chaves 'pdf', 'excel', 'exportar' estiveram presentes".format(
        elemento, len(result[column_name]), sum(result[column_name]))

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result