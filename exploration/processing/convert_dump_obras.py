from bs4 import BeautifulSoup
import pandas as pd
import codecs
from os import walk

def search_attribute(element, class_name):
    el = element.find('p', {'class': class_name})
    if el: 
        return el.getText()
    return None

def extract_data_from_file(file):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    names = []
    categories = [] 
    dates_beg = [] 
    dates_end = [] 
    stages = []

    for element in html.find_all('div', {'class': 'row'}):
        categories.append(search_attribute(element,'pCategoria'))
        dates_beg.append(search_attribute(element,'pDtInicio'))
        dates_end.append(search_attribute(element,'pDtTermino'))
        stages.append(search_attribute(element,'pCdObraSituacao'))
        
        name = element.find('a', href = True)
        if name: names.append(name.getText())
        else: names.appen(None)

    return names,categories,dates_beg,dates_end,stages

def main():
    filename = './Governador Valadares/obras/obras.html'
    file = codecs.open(filename, 'r', 'utf-8')
    name, category, date_beg, date_end, stage = extract_data_from_file(file)
    new_df = pd.DataFrame({'Nome': name, 'Tipo': category, 'Situacao': stage, 'Data Inicio': date_beg, 'Data Termino': date_end}) 
    new_df.to_csv('Governador Valadares/dados-processados/obras.csv')

main()