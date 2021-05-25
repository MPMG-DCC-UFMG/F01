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

def get_dates(ul):
    dates = ul.find_all('span')
    if dates:
        return dates[0].getText(), dates[1].getText()
    else: 
        return '', ''

def get_subject(ul):
        p = ul.find('p')
        if p: 
            return p.getText()
        else: 
            return ''

def extract_data_from_file(file, link_dec, num_dec, publication_date, signing_date, subject):
    html= BeautifulSoup(file.read(), features = 'html.parser')
    
    for element in html.find_all('div', {'class': 'well'}):
        
        h3 = element.find('h3').find('a')
        link_dec.append(original_url + h3['href'])
        num_dec.append(h3.getText())

        ul =  element.find('ul')
        sign_date, p_date = get_dates(ul)
        signing_date.append(sign_date)
        publication_date.append(p_date)
        subject.append(get_subject(ul))
            
    return link_dec, num_dec, publication_date, signing_date, subject
        

def main():
    dir = './Governador Valadares/legislacao'
    files = get_all_filenames_in_dir(dir)
    link_dec = [] 
    num_dec = [] 
    publication_date = [] 
    signing_date = [] 
    subject = []

    for f in files:
        file = codecs.open(dir + '/' +  f, 'r', 'utf-8')
        link_dec, num_dec, publication_date, signing_date, subject = extract_data_from_file(file, link_dec, num_dec,publication_date, signing_date, subject)
    
    new_df = pd.DataFrame({'urlDecreto': link_dec, 'numDecreto': num_dec, 
                        'DataPublicacao': publication_date, 'DataAssinatura': signing_date, 'Descricao': subject})
    new_df.to_csv('./Governador Valadares/dados-processados/legislacao.csv')

main()