from bs4 import BeautifulSoup
import chardet
import codecs
import os
import time
import pandas as pd

# <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

path = '/home/asafe/GitHub/Coleta_C01/Congonhas/despesas/2021/data/raw_pages/fe8c46064aec75d9021fa6f914bc7f46.html'
path3 = '/home/asafe/GitHub/Coleta_C01/Congonhas/despesas/2021/data/raw_pages/0a9c543860859c459adfabb46c364786.html'
path2 = '/home/asafe/Downloads/abc.html'
# file = codecs.open(path, 'r', 'latin-1')

# with open(path, encoding="utf8", errors='ignore') as f:
# f = codecs.open(path3, 'r', encoding="utf-8", errors='ignore')
# text = f.read()
# print(text)

# soup = BeautifulSoup(text, features="lxml",from_encoding="Windows-1252")

# metatag = soup.new_tag('meta')
# metatag.attrs['http-equiv'] = 'Content-Type'
# metatag.attrs['content'] = 'text/html; charset=utf-8'
# soup.head.append(metatag)

# source = soup.prettify("utf-8")
# with open("/home/asafe/Downloads/output.html", "wb") as file:
#     file.write(soup)

# print(source)

# import shlex, subprocess
# command_line = input()
# # /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
# args = shlex.split(command_line)
# print(args)

class Despesas:
    def __init__(self, files):
        self.files = files

class Empenhos(Despesas):

    def __init__(self, files, keywords_check):
        self.keywords_check = keywords_check

# Empenhos(files="asd",keywords_check="s")

# print("opa")
# print(Empenhos.files)

string  = """
<table cellspacing="0" class="table table-bordered table-sm dataTable no-footer" role="grid" style="margin-left: 0px; width: 637px;" width="100%"><thead>
<tr role="row"><th aria-controls="gridReceita" aria-label="Mês: Ordenar colunas de forma ascendente" class="sorting" colspan="1" rowspan="1" style="width: 81.8px;" tabindex="0">Mês</th><th aria-controls="gridReceita" aria-label="Receita: Ordenar colunas de forma descendente" aria-sort="ascending" class="sorting_asc" colspan="1" rowspan="1" style="width: 148.8px;" tabindex="0">Receita</th><th aria-controls="gridReceita" aria-label="Nome da Receita: Ordenar colunas de forma ascendente" class="sorting" colspan="1" rowspan="1" style="width: 100.8px;" tabindex="0">Nome da Receita</th><th aria-controls="gridReceita" aria-label="Previsto: Ordenar colunas de forma ascendente" class="text-right sorting" colspan="1" rowspan="1" style="width: 86.8px;" tabindex="0">Previsto</th><th aria-controls="gridReceita" aria-label="Arrecadado: Ordenar colunas de forma ascendente" class="text-right sorting" colspan="1" rowspan="1" style="width: 90.8px;" tabindex="0">Arrecadado</th><th aria-controls="gridReceita" aria-label="Acumulado: Ordenar colunas de forma ascendente" class="text-right sorting" colspan="1" rowspan="1" style="width: 0px; display: none;" tabindex="0">Acumulado</th></tr>
</thead></table>
"""

x = pd.read_html(string)
print(x)