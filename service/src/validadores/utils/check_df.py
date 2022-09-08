import numpy as np
from utils import checker

def contains_keyword(df, word):
    """
    Verifica se um dataframe possui uma coluna cujo nome contém uma palavra-chave especifica
    """
    # columns = [i.lower() for i in df.columns]
    i = 0
    if df is None:
        return False, word

    for column_name in df.columns:
        try:
            column_name = column_name.lower()
        except AttributeError:
            continue
        finder = column_name.find(word.lower())
        if finder != -1:
            return True, df.columns[i]
    
        i +=1
        
    print("the: ",word)
    return False, word

def infos_isvalid(df, column_name, threshold=0): 
    """
    Verifica se a quantidade de informações válidas no dataframe é maior que um valor de threshold.
    """
    
    if sum(df[column_name]) > threshold:
        return True
    else:
        return False

def files_isvalid(df, column_name, threshold=0): 
    """
    Verifica se a quantidade de arquivos válidos em um arquivo é maior (igual) que um valor de threshold.
    """
    
    for i in df[column_name]:
        if i >= threshold:
            return True
    return False

def check_all_values_of_column(df, keyword_check, typee='valor'):
    """
    Checa se uma coluna de um dataframe contém valores validos.

    Parameters
    ----------
    df : dataframe 
        Dataframe a ser verificado
    keyword_check : string 
        Coluna a ser verificada
    type  : 'valor', 'data', 'ano' or text
        Qual é o tipo do dado da coluna
        
    Returns
    -------
    Dataframe
        Dataframe original com uma columa "isvalid" com true ou false para cada entrada analisada.
    Boolean
        Se é verdade que existe algum valor válido na coluna, retorna true ou false.
    """
    
    if typee == 'valor':
        vfunc = np.vectorize(checker.check_value)
    if typee == 'data':
            vfunc = np.vectorize(checker.check_date)
    if typee == 'ano':
        vfunc = np.vectorize(checker.check_year)
    if typee == 'text':
        vfunc = np.vectorize(checker.check_description)

    valid = []
    df['isvalid'] = False    

    if not len(df):
        return df, False

    if keyword_check in df.columns:
        if typee == 'valor':
            if df[keyword_check].dtypes != float:
                df = checker.format_values(df, keyword_check)
        df['isvalid'] =  vfunc(df[keyword_check])
        valid.append(df['isvalid'].sum())

    isvalid = False
    for c in valid:
        if c >= (1):
            isvalid = True

    return df, isvalid

import re
def search_in_column(df, column_name, keywords):
    """
    Checa se uma coluna de um dataframe contém os valores procurados.

    Parameters
    ----------
    df : dataframe 
        Dataframe a ser verificado
    column_name : string 
        Coluna a ser verificada
    keywords  : string ou lista de string
        Palavras que se estiverem presentes validam uma entrada
        
    Returns
    -------
    Dataframe
        Dataframe original com uma columa "isvalid" com true ou false para cada entrada analisada.
    """
    df['isvalid'] = False
    if column_name in df.columns:

        if type(keywords) is str:
            vfunc = np.vectorize(checker.check_keyword)
            df['isvalid'] =  vfunc(df[column_name], keywords)

        elif type(keywords) is list:
            isvalid = []
            for value in df[column_name]:
                match = checker.check_any_keyword(value, keywords)
                isvalid.append(match)
            df['isvalid'] =  isvalid

    return df
