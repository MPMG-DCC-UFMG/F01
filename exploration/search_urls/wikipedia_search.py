# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

import wikipedia
import re

wikipedia.set_lang("pt")


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


def get_wiki_links(soup):
    """
    Search the wikipedia link for each city in Minas Gerais.

    Parameters
    ----------
    soup : BeautifulSoup object
        Object containing the page to be processed.
        
    Returns
    -------
    list of string
        List with the link to the wikipedia page of each city in Minas Gerais.

    """

    table = soup.find("table", {"class": "wikitable sortable"})
    wiki_links = ['https://pt.wikipedia.org/' + i.get('href') for i in table.find_all('a')]
    
    return wiki_links


def search_wiki_page(wiki_links, verbose=True):
    """
    Search the wikipedia page for links to the portals of each city.

    Parameters
    ----------
    wiki_links : list of string
        List with the link to the wikipedia page of each city in Minas Gerais.
    verbose: boolean, default True
        If true print log messages. 
        
    Returns
    -------
    list of string
        List with the link to the cities portal.

    """
    
    link_pref = []
    link_camara = []
    
    for link in wiki_links:

        if verbose:
            print(link)
        
        page = get_page(link)
        
        for i in page.find_all('tr'):
            if str(i).find('<td scope="row" style="vertical-align: top; text-align: left; font-weight:bold;">Sítio') != -1:
                tr = i
                break
        try:
            link_pref.append(tr.find_all('a',{'class':'external text'})[-2].get('href'))
            link_camara.append(tr.find_all('a',{'class':'external text'})[-1].get('href'))
        except:
            link_pref.append(tr.find_all('a',{'class':'external free'})[-2].get('href'))
            link_camara.append(tr.find_all('a',{'class':'external free'})[-1].get('href'))
        
    return link_pref, link_camara


def get_wikipedia_page(search):
    """
    Search for a wikipedia page that contains the search string

    Parameters
    ----------
    search : string
        Text to be found on wikipedia.
        
    Returns
    -------
    string
        Wikipedia page.

    """
    
    response = wikipedia.search(search)
    response = wikipedia.page(response[0])
    
    return response


def format_link (links):
    
    formated_link = []
    for link in links:
        formated_link.append(link.split('.gov.br')[0] + '.gov.br')
    
    return formated_link


def main_wikipedia_search(municipios):

    response = get_wikipedia_page(search="Lista de municípios de Minas Gerais por população")
    
    soup = get_page(response.url)
    wiki_links = get_wiki_links(soup)

    link_pref, link_camara = search_wiki_page(wiki_links)
    
    link_pref = format_link(link_pref)
    
    
    return link_pref, link_camara

path = '../../../persistence_area'

municipios = pd.read_csv("{}/municipios.csv".format(path))

link_pref, link_camara = main_portais_prefeitura(municipios)

df = pd.DataFrame({"municipios": municipios['municipios'],
                       'portal_prefeitura': link_pref,
                       'portal_camara': link_camara})


df.to_csv('{}/portal_prefeitura_camara.csv'.format(path), index=False)
