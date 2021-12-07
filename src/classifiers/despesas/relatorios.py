from utils import indexing
from re import T
import pandas as pd
import numpy as np
import sys
from utils import checker
from utils import path_functions
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
from utils import read


def predict_plano_plurianual(search_term = 'Empenhos',
    keywords=['Empenhos, despesa, empenhado, favorecido, valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])
    for file in html_files:
            print(file)

    if verbose:
        print('\nPredict Descrição:')

    # Cheking Descricao
    is_valid = False
    result = []
    
    return isvalid, result


# Link de acesso ao Plano Plurianual do município
# Link de acesso à Lei de Diretrizes Orçamentaria do município
# Link de acesso à Lei Orçamentária Anual do município
# Apresentação do balanço anual, com as respectivas demonstrações contábeis
# Relatórios da execução orçamentária e gestão fiscal