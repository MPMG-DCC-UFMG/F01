from bs4 import BeautifulSoup
import pandas as pd
import os


def read_content(path, folder, file):
    
    page = open("{}/{}/{}".format(path, folder, file), encoding="utf8").read()
    soup = BeautifulSoup(page, features="lxml")
    
    return soup


def list_to_text(soup):

    type = []
    text = []
    try:
        for i in soup.find("div", { "id" : "detalhes" }).findAll('li'):
            info = i.get_text().split(": ")
        
            if len(info) == 2:
                type.append(info[0].lower().replace("\n", ''))
                text.append(info[1])
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
    soup = BeautifulSoup(open(path), features="lxml")
    df = convert_html(soup)

    return df   


def one_list_to_csv (format_path):
    """
    Convert um elemento 'li' do html para um dataframe.
    """
    try: 

        df, type = convert_one_file(format_path)
        if type == 'list':
            return df
        
    except ValueError:
        pass

    return pd.DataFrame()

def all_lists_to_csv(paths, path_base, unwanted_name):

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

def concat_lists(files):

    if len(files) == 1:
        df = files[0]
    else:
        df = pd.concat(files)
    return df



def load_and_convert_files(path_base, paths, type):

    if type == 'html':
        
        if os.path.isfile("licitacoes.csv"):
            df = pd.read_csv("licitacoes.csv")
        else:
            df = all_lists_to_csv(paths, path_base, "licitacoes.csv")

    elif type == 'csv':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(path_base + i))

        df = concat_lists(list_csv)

    elif type == 'xls':

        list_xls = []
        for i in  paths:
            list_xls.append(pd.read_excel(path_base + i))

        df = concat_lists(list_xls)

    return df