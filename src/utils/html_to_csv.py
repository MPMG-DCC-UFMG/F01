from bs4 import BeautifulSoup
import pandas as pd
import os
import codecs
import tabula
from utils import read

def read_content(path, folder, file):

    try:
        file = codecs.open("{}/{}/{}".format(path, folder, file), 'r', 'utf-8')
        soup = BeautifulSoup(file, features="lxml")
    except:
        file = codecs.open("{}/{}/{}".format(path, folder, file), 'r', 'latin-1')
        soup = BeautifulSoup(file, features="lxml")
    
    return soup


def list_to_text(soup):

    type = []
    text = []
    try:
        for i in soup.find("div", { "id" : "detalhes" }).findAll('li'):
            info = i.get_text().split(": ")
            if len(info) >= 2:
                type.append(info[0].lower().replace("\n", ''))
                text.append(''.join(info[1:]))
            elif len(info) == 1:
                type.append(info[0].lower().replace("\n", ''))
                text.append("")
        df = pd.DataFrame([text], columns=type)

    except AttributeError:
        df = pd.DataFrame()
        pass

    return df

def convert_html(soup):
    type = 'None'
    try:
        df = pd.read_html(str(soup.table))[0]
        type = 'table'
    except ValueError:  
        df = list_to_text(soup)
        type = 'list'

    return df, type

def convert(all_files, path, folder):

    list_df = []
    for file in all_files:
        soup = read_content(path, folder, file)
        df = convert_html(soup)
        list_df.append(df)
    df = pd.concat(list_df)
    df = df.drop_duplicates()
    
    return df

def convert_one_file(path):
    soup = read.read_html(path)
    # soup = BeautifulSoup(open(path), features="lxml")
    df, type = convert_html(soup)
    return df, type   

def one_list_to_csv (format_path):
    """
    Convert um elemento 'li' do html para um dataframe.
    """
    try: 

        df, type = convert_one_file(format_path)
        if type == 'list' or type == 'table':
            return df
        
    except ValueError:
        pass

    return pd.DataFrame()

def all_lists_to_csv(paths):

    list_df = []
    for file_name in paths:
        new_df = one_list_to_csv(file_name)
        if(not new_df.empty):
            list_df.append(new_df)
    if (len(list_df)):              
        return pd.concat(list_df)
    else: 
        return pd.DataFrame()

def concat_lists(files):
    if len(files) == 0:
        df = pd.DataFrame()
    elif len(files) == 1:
        df = files[0]
    else:
        df = pd.concat(files)
    return df

def load_and_convert_files(paths, format_type):

    if format_type == 'html':
        # print(paths)
        df = all_lists_to_csv(paths)

    elif format_type == 'csv':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(i))

        df = concat_lists(list_csv)
    
    elif format_type == 'bat':

        list_csv = []
        for i in  paths:
            tabela = pd.read_csv(i)
            if ('Unnamed' in ' '.join(tabela.columns.values)):
                tabela.columns = tabela.loc[0].values
                tabela.drop(0 , inplace=True)
            # print("******",i)
            # print(tabela)
            # print(tabela.columns)
            list_csv.append(tabela)
        df = concat_lists(list_csv)
    
    elif format_type == 'doc':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(i))
        df = concat_lists(list_csv)

    elif format_type == 'xls':

        list_xls = []
        for i in  paths:
            list_xls.append(pd.read_excel(i))

        df = concat_lists(list_xls)

    elif format_type == 'pdf':

        number_entry_each_table = 1
        number_of_tables_per_doc = 1

        list_dfs = []
        for i in  paths:
            lista_tabelas = tabula.read_pdf(i, pages='all')
            for tabela in lista_tabelas:

                if ('Unnamed' in ' '.join(tabela.columns.values)):
                    tabela.columns = tabela.loc[0].values
                    tabela.drop(0 , inplace=True)

                    tabela = tabela.loc[:number_entry_each_table]

                list_dfs.append(tabela)
                print(tabela)

                break
                

        df = concat_lists(list_dfs)
    
    df = df.drop_duplicates()
    return df
