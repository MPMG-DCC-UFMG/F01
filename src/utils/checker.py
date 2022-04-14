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
    
    if data != '' and data != np.nan and data != None:
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
    
    if not isnumber:
        try: 
            converted = float(value)
            
            if converted == 0:
                return "Invalid Number"
            else:
                return True
            
        except ValueError:
            return False
    
    return isnumber 


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
