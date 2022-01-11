from utils import path_functions
from utils import indexing
from utils import check_df
from utils import read
import pandas as pd

# Possibilita a consulta de empenhos ou pagamentos por favorecido	
def predict_favorecido(search_term = 'Empenhos Pagamentos',
    keywords=['Pagamentos', 'despesa', 'Empenhos', 'favorecido', 'favorecidos', 'credor'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 100, job_name = '', verbose=False):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, filter_words)

    # Analyze 
    matches = []
    for path in html_files:
        soup = read.read_html(path)
        if soup.table:
            soup.table.extract()
        text = soup.getText()

        keyword_to_search =  [word.lower() for word in keywords if word.lower() in text.lower()] 
        
        if 'pagamentos' or 'empenhos' in keyword_to_search:
            if 'favorecido' or 'favorecidos' or 'credor' in keyword_to_search:
                matches.append(1)
        else:
            matches.append(1)

    result = pd.DataFrame({'files': html_files, 'matches': matches})

    #Check result 
    isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

    if verbose:
        print('\nPredict Favorecido:', isvalid)
    
    return isvalid, result
def explain(isvalid, result, column_name, elemento, verbose=False):

    print(isvalid)
    result = "Explain - Quantidade de entradas analizadas: {} . Quantidade de entradas que possuem o item '{}' válido: {}".format(
        len(result[column_name]), elemento, sum(result[column_name]))

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result