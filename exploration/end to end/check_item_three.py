# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import os
import nltk

path = '../../../persistence_area/gv'


def clean_text(text):
    
    text = text.replace("\n", ' ')
    text = re.sub(' +', ' ', text)
    text = text.lower()
    
    return text


def search_string(text, string):
    
    return text.find(string)


def search_pages(path, folder, string):
    
    pages = []
    files = os.listdir('{}/{}'.format(path, folder))
    
    for file in files:

        text, _ = read_html(path, folder, file)
        text = clean_text(text)
        match = search_string(text, string)

        if match != -1:
            pages.append((folder, file))
    
    return pages



def evaluate_folders (folders, pattern):
    
    result = [(i ,nltk.edit_distance(pattern, i)) for i in folders]
    result = sorted(result, key=lambda tup: tup[1])
    
    return result


def read_html(path, folder, file):
    
    page = open('{}/{}/{}'.format(path, folder, file))
    soup = BeautifulSoup(page, features="lxml")
    text = soup.get_text()
    
    return text, soup


def page_analyzer(path, folder, file):
    
    string='http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm'
    _, soup = read_html(path, folder, file)

    for i in urls:
        if search_string(str(soup).lower(), string) != -1:
            return True
    return False


def find_pattern(
    path, pattern, folder, verbose=True):
    
    folders = os.listdir(path)
    folders = evaluate_folders (folders, folder)
    
    for folder, similarity in folders:
        
        if verbose:
            print("Search pages in {} - Distance: {}".format(folder, similarity))
            
        files = os.listdir('{}/{}'.format(path, folder))
        for file in files:
            
            result = page_analyzer(path, folder, file)
                
            if result:
                return True
    return False


#item 3
pattern='http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm'
find_pattern(path, pattern, folder='Acesso a Informação', verbose=False)
