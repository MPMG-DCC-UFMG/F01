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
