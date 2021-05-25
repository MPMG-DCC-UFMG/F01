from bs4 import BeautifulSoup
import pandas as pd
import codecs
from os import walk

original_url = 'https://transparencia.valadares.mg.gov.br/'


def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

def search_attribute(element, tag, class_name):
    el = element.find(tag, {'class': class_name})
    if el: 
        return el.getText()
    return None

def extract_data_from_file(file,numDiario,descCaderno,dtPublicacao):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    for element in html.find_all('li', {'class': 'list-group-item'}):
        numDiario.append(search_attribute(element,'span', 'badge tamanho'))
        descCaderno.append(search_attribute(element,'h4', 'list-group-item-heading'))
        dtPublicacao.append(search_attribute(element,'span', 'publicacao-data'))
    
    return numDiario,descCaderno,dtPublicacao


def convert_to_csv(numDiario,descCaderno,dtPublicacao):
    dir = 'Governador Valadares/dados-processados/'
    new_df = pd.DataFrame({'numDiario': numDiario, 'descCaderno': descCaderno, 'dtPublicacao': dtPublicacao})
    new_df.to_csv(dir + 'diario.csv')

def main():
    dir = 'Governador Valadares/diario_eletronico'
    files = get_all_filenames_in_dir(dir)
    
    numDiario = [] 
    descCaderno = []
    dtPublicacao = []
    
    for f in files:
        file = codecs.open(dir + '/' +  f, 'r', 'utf-8')
        numDiario,descCaderno,dtPublicacao = extract_data_from_file(file,numDiario,descCaderno,dtPublicacao)
    
    convert_to_csv(numDiario,descCaderno,dtPublicacao)

main()