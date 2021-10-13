from bs4 import BeautifulSoup

def read_html(path):

    text = open(path, encoding='latin-1').read()
    soup = BeautifulSoup(text, features="lxml",from_encoding="latin-1")

    return soup

def read_file(path):

    return open(path, encoding='iso-8859-15').read()