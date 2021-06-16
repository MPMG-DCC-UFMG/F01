from bs4 import BeautifulSoup
import pandas as pd
import os


def read_content(path, folder, file):
    
    page = open("{}/{}/{}".format(path, folder, file)).read()
    soup = BeautifulSoup(page, features="lxml")
    
    return soup


def convert_html(soup):
    
    df = pd.read_html(str(soup.table))[0]
    
    return df


def convert(all_files, path, folder):

    list_df = []

    for file in all_files:

        soup = read_content(path, folder, file)
        df = convert_html(soup)
        list_df.append(df)
    
    df = pd.concat(list_df)
    df = df.drop_duplicates()
    
    return df
