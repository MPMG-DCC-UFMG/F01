from bs4 import BeautifulSoup
import chardet
import codecs

def read_html(path):
    try:
        file = codecs.open(path, 'r', 'utf-8', errors='ignore')
        soup = BeautifulSoup(file, features="lxml",from_encoding="utf-8")
        return soup
    except:
        file = codecs.open(path, 'r', 'latin-1', errors='ignore')
        soup = BeautifulSoup(file, features="lxml",from_encoding="latin-1")
        return soup
    # text = codecs.open(path, encoding='latin-1', errors='ignore').read()
    # soup = BeautifulSoup(text, features="lxml",from_encoding="latin-1")


def read_file(path):

    return open(path, encoding='iso-8859-15').read()


def auto_read_html(path):

    rawdata = open(path, 'rb').read()
    # file = codecs.open(path, 'r', 'latin-1').read()
    encoding = chardet.detect(rawdata)['encoding']

    soup = BeautifulSoup(rawdata, features="lxml",from_encoding=encoding)
    return soup


        # try:
        #     file = codecs.open(filename, 'r', 'utf-8')
        #     markup = BeautifulSoup(file.read(),  "html.parser" )
        # except:
        #     file = codecs.open(filename, 'r', 'latin-1')
        #     markup = BeautifulSoup(file.read(),  "html.parser" )

    