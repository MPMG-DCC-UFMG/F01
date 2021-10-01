import pandas as pd
import os
from pathlib import Path
import json
import codecs

from utils import table_to_csv

def agg_type(paths):

    files = {'csv': [], 'xls': [], 'html': [], 'pdf': [], 'doc':[]}

    for path in paths:

        suffix = Path(path).suffixes[0]
        
        if suffix == ".xls":
            files['xls'].append(path)
        elif suffix == '.csv':
            files['csv'].append(path)
        elif (suffix == ".html") or (suffix == '.xml'):
            files['html'].append(path)
        elif (suffix == ".pdf"):
            files['pdf'].append(path)
        elif (suffix == ".doc") or (suffix == '.docx'):
            files['doc'].append(path)

    return files

def get_extension(path):
    return path.split('.')[-1]

def get_name(path):
    return path.split('/')[-1]

def format_path(path):
    path = path.split(os.sep)
    return os.sep.join(path[3: len(path)-1])

def get_paths(indexes):

    paths = []

    for i in indexes:

        extensions = get_extension(str(i[2]))
        path = format_path (str(i[2]))
        paths.append((path, extensions))
    return paths

def check_columns(df, word):
    """
    Verifica se um dataframe possui uma coluna cujo nome contém uma palavra-chave
    """

    columns = [i.lower() for i in df.columns]
    i = 0
    for column_name in columns:

        finder = column_name.find(word)
       
        if finder != -1:
            return True, columns[i]
    
        i +=1
    return False, word


def filter_paths(paths, word):
    """
    Filtra os caminhos retornados pelo indexador por uma palavra-chave
    """
    filtered_paths = []
    for i in paths:

        if i[0].find(word) != -1:
            filtered_paths.append(i)
    return filtered_paths

def one_list_to_csv (format_path):
    """
    Convert um elemento 'li' do html para um dataframe.
    """
    try: 

        df, type = table_to_csv.convert_one_file(format_path)
        if type == 'list':
            return df
        
    except ValueError:
        pass

    return pd.DataFrame()

def list_to_csv(paths, path_base, unwanted_name):

    list_df = []
    for path, type in paths:
        if type == 'html':
            files = os.listdir(path_base + os.sep + path)
            for file in files:
                format_path = "{}/{}/{}".format(path_base, path, file)
                if not os.path.isfile(unwanted_name):
                    new_df = one_list_to_csv(format_path)
                    
                    if(not new_df.empty):
                        list_df.append(new_df)
                    
    return pd.concat(list_df)


def get_url(path_base, filename):

    file_description = path_base + "/" + format_path(filename) + "/" + 'file_description.jsonl'
    arquivo = codecs.open(file_description, 'r', 'utf-8').readlines()
    for line in arquivo:
        json = eval(line)
        if (json['file_name'] == get_name(filename)):
            return json['url']