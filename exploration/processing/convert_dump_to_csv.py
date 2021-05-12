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

def extract_data_from_file(file):
    html= BeautifulSoup(file.read())
    urls = []
    dates = []
    desc = []
    title = []
    for a in html.find_all('a', href=True):
        urls.append(original_url + a['href'])
    for span in  html.find_all('span', {"class": "data"}):
        dates.append(span.getText())
    for p in  html.find_all('p', {"class": "descricao"}):
        desc.append(p.getText())
    for h4 in  html.find_all('h4', {"class": "list-group-item-heading"}):
        title.append(h4.getText())
    return urls, dates, desc, title

def convert_to_csv(f, urls, dates, desc, title):
    print(desc, title)
    new_df = pd.DataFrame({'Urls': urls, 'Data': dates, 'Descricao': desc, 'Titulo': title})
    new_df.to_csv('csvs/' + f.replace('.html', ''))

def main():
    dir = 'dump_gov_valadares'
    files = get_all_filenames_in_dir(dir)
    for f in files:
        file = codecs.open(dir + '/' +  f, 'r', 'utf-8')
        urls, dates, desc, title = extract_data_from_file(file)
        convert_to_csv(f, urls, dates, desc, title)

main()