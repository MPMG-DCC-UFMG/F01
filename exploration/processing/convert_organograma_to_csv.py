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

def extract_data_from_file(file,names, types, addresses, list_of_in_charge, emails, business_hours, descriptions, responsabilities):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    
    for element in html.find_all('div', {'class': 'divDados'}):    
        names.append(search_attribute(element, 'h5', 'nmUnidade'))    
        types.append(search_attribute(element, 'h4', 'nmUnidadeTipo'))    
        addresses.append(search_attribute(element, 'p', 'dsEndereco'))    
        list_of_in_charge.append(search_attribute(element, 'p', 'nmResponsavelUnidade'))  
        emails.append(search_attribute(element, 'p', 'edEmailUnidade'))  
        business_hours.append(search_attribute(element, 'p', 'dsHorarioFuncionamento'))  
        descriptions.append(search_attribute(element, 'div', 'dsUnidade'))  
        responsabilities.append(search_attribute(element, 'div', 'dsCompetencias'))  

    return names, types, addresses, list_of_in_charge, emails, business_hours, descriptions, responsabilities


def main():
    dir_dump = 'Governador Valadares/organograma'
    dir_processed = 'Governador Valadares/dados-processados'    

    names = []
    types = []
    addresses = [] 
    list_of_in_charge = [] 
    emails = [] 
    business_hours = [] 
    descriptions = []
    responsabilities = []

    file = codecs.open(dir_dump + '/organograma.html', 'r', 'utf-8')
    names, types, addresses, list_of_in_charge, emails, business_hours, descriptions, responsabilities = extract_data_from_file(file, names, 
                                                    types, addresses, list_of_in_charge, emails, business_hours, descriptions, responsabilities)
    
    new_df = pd.DataFrame({'descUnidade': names, 'descTipo': types, 'descDescricao': descriptions, 'descCompetencia': responsabilities,
                            'descResponsavel': list_of_in_charge, 'descEmail': emails, 'descHorario': business_hours, 'enderecos': addresses})
    new_df.to_csv(dir_processed + '/' + 'organograma.csv')



main()