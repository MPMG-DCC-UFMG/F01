# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


def get_page(query, lower=False):
    """
    Search the wikipedia link for each city in Minas Gerais.

    Parameters
    ----------
    query : string
        Query used to fetch the page.
    lower : boolean, default False
        If true, the beuatiful soup object is returned with all lower case characters.
        
    Returns
    -------
    BeuatifulSoup object
        Result of the requested query.

    """

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    try:
        page = requests.get(query, headers=headers)
    except requests.exceptions.Timeout:
        print ("Timeout occurred")
    
    if lower:
        soup = BeautifulSoup(page.text.lower(),features="lxml")
    else:
        soup = BeautifulSoup(page.text,features="lxml")
    
    return soup


def googlesearch(search, number_results=5, language_code='pt'):

    search = search.replace(" ", "+")
    query = 'https://www.google.com/search?q={}&num={}&hl={}'.format(search, number_results+1,language_code)
    
    soup = get_page(query, lower=False)
    
    return soup


def find_links(soup):
    
    divs = soup.find_all('div', attrs={'class': 'g'})
    urls = []
    
    for div in divs:
    
        link = div.find('a', href=True)
        title = div.find('h3')

        if link and title:
            urls.append(link['href'])
            
    return urls


def find_all_links(municipios, verbose=True):

    urls = []
    for index, value in municipios.iterrows():
    
        search = "\"Portal Transparência {} MG\"".format(value['municipios'])
        
        if verbose:
            print(search)
    
        soup = googlesearch(search, number_results=5, language_code='pt')
        urls.append(find_links(soup))
        
        time.sleep(10)
        
    return urls


path = '../../../persistence_area'

municipios = pd.read_csv("{}/municipios.csv".format(path))
urls = find_all_links(municipios)

df['transparencia'] = urls

df2 = df['transparencia'].str.split(',', n=5, expand=True)

df = pd.concat([df, df2], axis=1)
df = df.rename(columns={0: 'link_1', 1: 'link_2', 2: 'link_3', 3: 'link_4', 4: 'link_5', 5: 'link_6'})

del df['transparencia']

del df['wiki_links']

df.to_csv("{}/google_search.csv".format(path), index=False)
