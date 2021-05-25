#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

def format_targets():
    
    targets_for_text = ['câmara', 'legislativo', 'controladoria-geral', 'plurianual', 'despesas',
                   'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                   'convênios', 'viagens', 'concurso', 'contas públicas', 'obras públicas',
                   'portal da transparência', 'transparência']
    
    #targets_for_text = [stemmer.stem(i) for i in targets_for_text]
    targets = '|'.join(targets_for_text)
    
    return targets, targets_for_text

def pontuar_texto(text, targets):
    
    find = re.findall(targets, text)
    
    return find

def pontuar_os_municipios(df, targets):

    count = 0
    for municipio in df.loc[:, 'Município']:
        name = 'portais/' + str(count) + '.html'
        
        try:
            with open(name, 'r') as arq:
                
                page = arq.read()
                text = BeautifulSoup(page, "html5lib").get_text().lower()
                
                #if text != '':
                #    text = remove_noise(text)
                #    text = stemming(text)
                    
                if len(text) < 300:
                    df.loc[count, "consegui_html"] = 0
                else: 
                    df.loc[count, "consegui_html"] = 1

                portal_estadual = re.findall('portaltransparencia.gov.br', df.loc[count, 'Portal da Transparência'])
                if portal_estadual:
                    df.loc[count, "consegui_html"] = None

                find_targets = pontuar_texto(text, targets)
                for palavra in find_targets:
                    df.loc[count, palavra] += 1
            count += 1
        except IndexError:
            count += 1
            continue
        except FileNotFoundError:
            count+=1
            continue
    return df

def main(df, train=True):
    
    df['Link Correto'] = df['Link Correto'].replace(['x'], 1)
    df['Link Correto'].fillna(0, inplace=True)
    
    df.loc[:, "consegui_html"] = None
    
    targets, targets_for_text = format_targets()
    
    df[targets_for_text] = 0
    
    df = pontuar_os_municipios(df, targets)

    df = df.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    if train:
        df = df.loc[ : 301, :]
        df = df.dropna(subset=['consegui_html'])
    
    result_search = df['consegui_html']
    del df['consegui_html']
    
    return df, result_search

