from bs4 import BeautifulSoup

def read_html(path):

    soup = BeautifulSoup(open(path), features="lxml",from_encoding="utf-8")

    return soup

def read_file(path):

    return open(path, encoding='iso-8859-15').read()