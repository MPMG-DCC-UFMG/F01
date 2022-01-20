# Empenhos

from utils import indexing
import pandas as pd
import numpy as np
import sys
from utils import checker
from utils import path_functions
import pandas as pd
import numpy as np
import warnings
from utils import read

sys.path.insert(1, '../')

PAGAMENTOS = {
    'valor' : ['Liquidado', 'Pago', 'Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 'Empenhado no período (R$)', 'Pago no período (R$)'],
    'data' : ['ano'],
    'favorecido' : ['Favorecido', 'Credor'],
    'empenho_referencia' : ['Número', 'Empenho', 'Empenho/ Processo']
}

warnings.filterwarnings('ignore')

def list_to_text(soup):

    type = []
    text = []
    try:
        for i in soup.find('div', { 'id' : 'detalhes' }).findAll('li'):
            info = i.get_text().split(': ')
        
            if len(info) == 2:
                type.append(info[0].lower().replace('\n', ''))
                text.append(info[1])
            elif len(info) == 1:
                type.append(info[0].lower().replace('\n', ''))
                text.append('')

        df = pd.DataFrame([text], columns=type)

    except AttributeError:
        df = pd.DataFrame()
        pass

    return df

def convert_html_table(soup):
    type = 'None'
    try:
        # Deleting <tfoot> element 
        if soup.tfoot:
            soup.tfoot.extract()
        df = pd.read_html(str(soup.table))[0]
        type = 'table'
    except ValueError:
        df = list_to_text(soup)
        type = 'list'
    
    return df, type

def convert_to_df(all_files):

    """
    Recebe arquivos html, concatena as tabelas e retorna em um dataframe
    """

    list_df = []
    for file in all_files:

        soup = read.read_html(file)
        df, _ = convert_html_table(soup)
        list_df.append(df)

    df = pd.DataFrame()
    if(len(list_df)):
        df = pd.concat(list_df)
        df = df.drop_duplicates()

    return df

def check_all_values(df, columns_name):

    """
    Checa se uma taxa determinada (0 ... 1.0) de valores em uma coluna de um dataframe contem valores válidos,
    """

    vfunc = np.vectorize(checker.check_value)
    valid = []
    
    df['isvalid'] = False    
    for valor in columns_name:
        if valor in df.columns:
            if df[valor].dtypes != float:
                df = checker.format_values(df, valor)
            df['isvalid'] =  vfunc(df[valor])
            valid.append(df['isvalid'].sum())

    isvalid = False
    for c in valid:
        if c > (len(df.index)/2):
            isvalid = True
    return df, isvalid

def check_all_description(df, columns_name):

    vfunc = np.vectorize(checker.check_description)
    valid = []
    
    df['isvalid'] = False
    for i in columns_name:
        if i in df.columns:
            df['isvalid'] =  vfunc(df[i])
            valid.append(df['isvalid'].all())
            
    return df, any(valid)
    
def check_all_year(df, column='Ano'):
    
    vfunc = np.vectorize(checker.check_year)
    df['isvalid'] =  vfunc(df[column])
    
    return df, df['isvalid'].all()

def predict_valor(search_term = 'Pagamentos',
    keywords=['Pagamentos', 'despesa', 'empenhado', 'valor'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 1000, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths(html_files, filter_words)

    result = convert_to_df(html_files)
    
    # Cheking valor
    result, isvalid = check_all_values(result, columns_name=PAGAMENTOS['valor'])

    if verbose:
        print('\nPredict Valor:', isvalid)
        
    return isvalid, result

def predict_data(search_term = 'Pagamentos',
    keywords=['Pagamentos', 'despesa', 'empenhado', 'pago'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 1000, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths(html_files, filter_words)

    result = convert_to_df(html_files)

    # Cheking Data
    if 'Data' in result.columns:
        vfunc = np.vectorize(checker.check_date)
        result['isvalid'] = vfunc(result['Data'])
        isvalid = result['isvalid'].all()

    elif 'Ano' in result.columns:
        result, isvalid = check_all_year(result, column='Ano')

    elif 'Data do pagamento' in result.columns:
        vfunc = np.vectorize(checker.check_date)
        result['isvalid'] = vfunc(result['Data do pagamentos'])
        isvalid = result['isvalid'].all()
    else:
        result['isvalid'] = False
        isvalid = False

    if verbose:
        print('\nPredict Data:', isvalid)
    
    return isvalid, result

def predict_favorecido(search_term = 'Pagamentos',
    keywords=['Pagamentos', 'despesa', 'empenhado', 'favorecido', 'credor'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 100, job_name = '', verbose=False):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths(html_files, filter_words)

    if verbose:
        print('\nPredict Favorecido:')

    result = convert_to_df(html_files)

    # Cheking Descricao
    result, isvalid = check_all_description(result, columns_name=PAGAMENTOS['favorecido'])
    
    return isvalid, result


def predict_empenho_referencia(search_term = 'Pagamentos',
    keywords=['Empenhos', 'Pagamentos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_words=['despesas', 'empenhos', 'pagamentos'] , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths(html_files, filter_words)

    result = convert_to_df(html_files)

    # Cheking Descricao
    result, isvalid = check_all_description(result, columns_name=PAGAMENTOS['empenho_referencia'])

    if verbose:
        print('\nPredict Empenho de Referência:', isvalid)
    
    return isvalid, result


def explain(isvalid, result, column_name, elemento, verbose=False):

    print(isvalid)
    result = "Explain - Quantidade de entradas analizadas: {} . Quantidade de entradas que possuem o item '{}' válido: {}".format(
        len(result[column_name]), elemento, sum(result[column_name]))

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result