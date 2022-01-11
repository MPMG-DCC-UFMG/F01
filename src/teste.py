from bs4 import BeautifulSoup
import chardet
import codecs
import os

# <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

path = '/home/asafe/GitHub/Coleta_C01/Congonhas/despesas/2021/data/raw_pages/fe8c46064aec75d9021fa6f914bc7f46.html'
path3 = '/home/asafe/GitHub/Coleta_C01/Congonhas/despesas/2021/data/raw_pages/0a9c543860859c459adfabb46c364786.html'
path2 = '/home/asafe/Downloads/abc.html'
# file = codecs.open(path, 'r', 'latin-1')


# with open(path, encoding="utf8", errors='ignore') as f:
# f = codecs.open(path3, 'r', encoding="utf-8", errors='ignore')
# text = f.read()
# print(text)


keywords='Pagamentos asdasd asd asd asd asd asd asd credor'
teste = ['asdasd', 'b']

print(['a' for word in teste if keywords.count(word)])

print(any(word in keywords for word in teste))


# if any():
#     print(teste)

# f.write(s1)

# soup = BeautifulSoup(text, features="lxml",from_encoding="Windows-1252")

# metatag = soup.new_tag('meta')
# metatag.attrs['http-equiv'] = 'Content-Type'
# metatag.attrs['content'] = 'text/html; charset=utf-8'
# soup.head.append(metatag)

# source = soup.prettify("utf-8")
# with open("/home/asafe/Downloads/output.html", "wb") as file:
#     file.write(soup)

# print(source)


