import codecs
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

file = codecs.open('/home/asafe/GitHub/Coleta_F01/governador_valadares/prefeitura/data/raw_pages/56e49a4e6f2a8456f80c0efc03acd703.html', 'r', 'latin-1')
try:
    markup = BeautifulSoup(file.read(),  "html.parser" )
except TypeError:
    print('deu erro')