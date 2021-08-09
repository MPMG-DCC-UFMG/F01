from bs4 import BeautifulSoup
import pandas as pd
import codecs
def convert(filepath):

    soup = BeautifulSoup(codecs.open(filepath, 'r', 'utf-8').read(), features="lxml")
    df = pd.read_html(str(soup.table))[0]

    return df
