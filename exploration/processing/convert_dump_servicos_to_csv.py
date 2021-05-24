from bs4 import BeautifulSoup
import pandas as pd
import codecs
from os import walk

def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

def search_attribute(element, tag, class_name):
    el = element.find(tag, {'class': class_name})
    if el: 
        return el.getText().replace(',', '')
    return None

def search_inside_tag(element, tag, class_name, child_tag):
    el = element.find(tag, {'class': class_name})
    if el:
        child = el.find(child_tag)
        if child: return child.getText().replace(',', '')
    
    return None

def extract_data_from_file(file,category, department, title, requirements, documents, description):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    for element in html.find_all('div', {'class': 'servico'}):
        category.append(search_attribute(element,'p', 'cls-categoria'))
        department.append(search_attribute(element,'p', 'cls-unidade'))
        title.append(search_attribute(element,'h4', 'list-group-item-heading'))
        requirements.append(search_inside_tag(element, 'div', 'divExigencias', 'p'))    
        documents.append(search_inside_tag(element, 'div', 'divDocumentos', 'p'))    
        description.append(search_inside_tag(element, 'div', 'divDescricao', 'p'))    
    
    return category, department, title, requirements, documents, description


def main():
    dir_dump = 'Governador Valadares/servicos'
    dir_processed = 'Governador Valadares/dados-processados'    

    files = get_all_filenames_in_dir(dir_dump)
    category = []
    department = [] 
    title = [] 
    requirements = [] 
    documents = [] 
    description = []
    
    for f in files:
        file = codecs.open(dir_dump + '/' +  f, 'r', 'utf-8')
        category, department, title, requirements, documents, description = extract_data_from_file(file,category, department, 
                                                                                        title, requirements, documents, description)
    
    new_df = pd.DataFrame({'descCategoria': category, 'descUnidade': department, 'descGuiaServ': title, 
                            'descExigencia': requirements, 'descDocumento': documents, 'descricao': description})
    new_df.to_csv(dir_processed + '/' + 'servicos.csv')



main()