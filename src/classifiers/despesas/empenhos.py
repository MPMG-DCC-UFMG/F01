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

DESPESAS = {
    'numero' : ['Número', 'Empenho', 'Empenho/ Processo'],
    'descricao' : ['Unidade', 'Fornecedor','Ação', 'Descrição', 'Tipo'],
    'favorecido' : ['Favorecido', 'Credor'],
    'valor' : ['Empenhado', 'Liquidado', 'Pago', 'Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 'Empenhado no período (R$)']
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

def convert(all_files):

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

def predict_numero(search_term = 'Empenhos',
    keywords=['Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])
    # for file in html_files:
    #     print(file)

    if verbose:
        print('\nPredict Número:')

    result = convert(html_files)
    # print(result.columns)
    # Cheking valor
    result, isvalid = check_all_values(result, columns_name=DESPESAS['numero'])
        
    return isvalid, result


def predict_valor(search_term = 'Empenhos',
    keywords=['Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])

    if verbose:
        print('\nPredict Valor:')

    result = convert(html_files)
    # Cheking valor
    result, isvalid = check_all_values(result, columns_name=DESPESAS['valor'])
        
    return isvalid, result

def predict_data(search_term = 'Empenhos',
    keywords=['Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])

    if verbose:
        print('\nPredict Data:')

    result = convert(html_files)
    # Cheking Data
    if 'Data' in result.columns:
        vfunc = np.vectorize(checker.check_date)
        result['isvalid'] = vfunc(result['Data'])
        isvalid = result['isvalid'].all()
    elif 'Ano' in result.columns:
        result, isvalid = check_all_year(result, column='Ano')
    elif 'Data do empenho' in result.columns:
        vfunc = np.vectorize(checker.check_date)
        result['isvalid'] = vfunc(result['Data do empenho'])
        isvalid = result['isvalid'].all()
    else:
        result['isvalid'] = False
        isvalid = False
    
    return isvalid, result

def predict_favorecido(search_term = 'Empenhos',
    keywords=['Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):

    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])

    if verbose:
        print('\nPredict Favorecido:')

    result = convert(html_files)

    # Cheking Descricao
    result, isvalid = check_all_description(result, columns_name=DESPESAS['favorecido'])
    
    return isvalid, result


def predict_descricao(search_term = 'Empenhos',
    keywords=['Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor'],
    filter_word='despesas' , path_base='/home', num_matches = 100, job_name = '', verbose=False):
    
    #Search all files using keywords
    html_files = indexing.get_files_to_valid(
        search_term, keywords, num_matches,
        job_name, path_base)

    html_files = path_functions.filter_paths2(html_files, ['despesas', 'empenhos'])

    if verbose:
        print('\nPredict Descrição:')

    result = convert(html_files)

    # Cheking Descricao
    result, isvalid = check_all_description(result, columns_name=DESPESAS['descricao'])
    
    return isvalid, result


def explain(isvalid, result, column_name, elemento, verbose=False):

    print(isvalid)
    result = "Explain - Quantidade de entradas analizadas: {} . Quantidade de entradas que possuem o item '{}' válido: {}".format(
        len(result[column_name]), elemento, sum(result[column_name]))

    if verbose:
        print('\n \t Predict -', isvalid)
        print('\t', result)

    return result