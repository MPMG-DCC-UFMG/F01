import os
import pandas as pd
import numpy as np
import datetime
import re

import warnings
warnings.filterwarnings("ignore")


def format_values(df, column_name):
    """
    Format a column of a dataframe 
        - R\$ to ''
        - '.' to ''
        - ',' to point
        - Converting non-digits to 0

    Parameters
    ----------
    df : dataframe
        Data to be formated
    column_name : string
        what is the dataframe column that should be formatted
        
    Returns
    -------
    Boolean
        formatted dataframe
    """
    
    df[column_name] = df[column_name].astype(str)

    df[column_name] = df[column_name].str.replace("R\$", '')
    df[column_name] = df[column_name].str.replace(".", '')
    df[column_name] = df[column_name].str.replace(",", '.')

    # Converting non-digits to 0
    df[column_name] = df[column_name].str.replace(r"\D*", '0')

    df[column_name] = df[column_name].astype(float)

    return df

def isvalid(data):
    """
    Checked if data is valid
         
        - is not empty string
        - is not nan
        - is not none
    Parameters
    ----------
    value : string, float or int
        Data to be verified
        
    Returns
    -------
    Boolean
        If value is valid, return true else false.
    """
    if data != '' and data != np.nan and data != None and data is not np.nan:
        return True
    
    return False


def check_value(value):
    """
    Checked if value is valid.
         
        - float or int
        - different of zero
    Parameters
    ----------
    value : string, float or int
        value to be verified
        
    Returns
    -------
    Boolean
        If value is valid, return true else false.
    """
    
    isnumber = isinstance(value, (int, float))
    
    if isnumber:
        return value != 0

    else:
        try: 
            converted = float(value)
            
            if converted == 0:
                return "Invalid Number"
            else:
                return True
            
        except ValueError:
            return False
    


def search_splitter(string):
    """
    Check which is the separator character of the date string
    Parameters
    ----------
    string : string
        String containing a date
        
    Returns
    -------
    string
        Splitter identified.
    """
    
    if '/' in string:
        return '/'
    elif '-' in string:
        return '-'


def check_date(date):
    """
    Check if the string is a valid date
    Parameters
    ----------
    date : string
        String containing a date
        
    Returns
    -------
    Boolean
        If date is valid, return true else false.
    """
    if type(date) == float:
        return False

    try :
        splitter = search_splitter(date)
        day, month, year = date.split(splitter)
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        return False
    
    return True


def check_year(ano):
    
    if (ano > datetime.datetime.now().year) and ano < 2000:
        return False
    return True

def check_competencia(date):
    """
    Check if the string is a valid date with MM/YY
    Parameters
    ----------
    date : string
        String containing a date MM/YY
        
    Returns
    -------
    Boolean
        If date is valid, return true else false.
    """
    
    splitter = search_splitter(date)
    month, year = date.split(splitter)
    day = 1

    try :
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        return False
    
    return True

def check_name(name):
    """
    Check if the name is a valid name.
    Parameters
    ----------
    name : string
        String containing a name.
        
    Returns
    -------
    Boolean
        If name is valid, return true else false.
    """
    
    return re.match("[Aa-Zz]+", name)


def check_description(description):
    """
    Check if the description is a valid.
    Parameters
    ----------
    description : string
        String containing a description.
        
    Returns
    -------
    Boolean
        If name is valid, return true else false.
    """
    
    return isvalid(description)

def check_keyword(value, keyword):
    """
    Chega se uma dada palavra chave aparece em uma string.
    Parameters
    ----------
    value : string
        String a ser examinada.
    keyword : string
        String a ser encontrada
        
    Returns
    -------
    Boolean
        Se encontrar retorna true se não false.
    """
    value = str(value)
    return re.search(keyword, value, re.IGNORECASE) != None


def check_any_keyword(value, keywords):
    """
    Chega se uma alguma palavra chave aparece em uma string.
    Parameters
    ----------
    value : string
        String a ser examinada.
    keywords : list of string
        Lista de strings a serem encontradas
        
    Returns
    -------
    Boolean
        Se encontrar retorna true se não false.
    """
    value = str(value)
    return any([re.search(k, value, re.IGNORECASE) != None for k in keywords])