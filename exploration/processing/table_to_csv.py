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


def table_to_csv(all_files, path, folder):

    list_df = []

    for file in all_files:

        soup = read_content(path, folder, file)
        df = convert_html(soup)
        list_df.append(df)
    
    df = pd.concat(list_df)
    df = df.drop_duplicates()
    
    return df


def main_table_to_csv(path, folder):
    
    all_files = os.listdir("{}/{}".format(path, folder))
    df = table_to_csv(all_files, path, folder)
    df.to_csv('{}/{}.csv'.format(path, folder), index=False)


path = '../../../persistence_area/gv'
directory='despesas-empenho'
main_table_to_csv(path, directory)
