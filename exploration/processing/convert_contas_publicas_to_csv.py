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

def search_inside_tag(element, tag, class_name, child_tag):
    el = element.find(tag, {'class': class_name})
    if el:
        child = el.find(child_tag)
        if child: return child.getText().replace(',', '')
    
    return None

def search_attribute(element, tag, class_name):
    el = element.find(tag, {'class': class_name})
    if el: 
        return el.getText().replace(',', '')
    return None

def extract_data_from_file(file, names, months, years, publication_dates, urls):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    
    for element in html.find_all('ul', {'class': 'list-group'}):
        names.append(search_attribute(element, 'span', 'nome_rel'))    
        months.append(search_attribute(element, 'p', 'periodo'))    
        years.append(search_attribute(element, 'p', 'ano'))    
        publication_dates.append(search_attribute(element, 'span', 'data')) 
        urls.append(original_url + html.find('a', href = True)['href'])
        
    return  names, months, years, publication_dates, urls

def main():
    dir = './Governador Valadares/contas-publicas'
    files = get_all_filenames_in_dir(dir)
    names = []
    months = [] 
    years = []
    publication_dates = []
    urls = []

    for f in files:
        file = codecs.open(dir + '/' +  f, 'r', 'utf-8')
        names, months, years, publication_dates, urls = extract_data_from_file(file, names, months, years, publication_dates, urls)
    
    new_df = pd.DataFrame({'Nome': names, 'DataPublicacao': publication_dates, 'Ano': years, 
                        'Periodo': months, 'Urls': urls})
    new_df.to_csv('./Governador Valadares/dados-processados/contas_publicas.csv')

main()