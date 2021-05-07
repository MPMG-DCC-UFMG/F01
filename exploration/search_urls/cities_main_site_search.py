# Extracts all possible TP links from the main website of each city in Minas Gerais
import pandas as pd
import requests 
import re
from time import sleep
from bs4 import BeautifulSoup

targets_for_text = ['Transparência', 'TRANSPARÊNCIA', 'TRANSPARENCIA', 'transparencia', 'Transparencia', 'transparência']
targets_for_link = ['Transparência', 'TRANSPARÊNCIA', 'TRANSPARENCIA', 'transparencia', 'Transparencia', 'transparência']
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}
delimiter = '; '

# Makes a request with the url passed as param and returns the respective html 
def get_html(url):
    s = requests.Session()
    r = s.get(url)
    sleep(0.1), print("Trying to connect to ", url)
    return BeautifulSoup(r.text)

# Returns the intersection of both array of urls 
def get_most_likely(resp1, resp2):
    intersection_set = set.intersection(set(resp1), set(resp2))
    return list(intersection_set)

# Returns relevant urls found on cities main site
def get_url(url):
  max_retries = 3
  retries = max_retries
  resp1 = []
  resp2 = [] 
  possible_urls = []
  most_likely_urls = []

  while (retries):
    retries -= 1
    try:
      markup = get_html(url)
      for a in markup.find_all(text= targets_for_text, href=True):
          if a not in resp1: resp1.append(a['href'])
      
      urls = markup.find_all('a')
      for tag in urls:
          url = tag.get('href',None)
          for t in targets_for_link:
            if url is not None and t in url and url not in resp2: 
              resp2.append(url)
      
      most_likely_urls = get_most_likely(resp1, resp2)
      possible_urls = resp1 + resp2 
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, TimeoutError):
      print("Failed to connect to ", url, ". Attempt:", max_retries - retries, " of ", max_retries)
    
    else: break
  
   return delimiter.join(possible_urls), delimiter.join(most_likely_urls)

def main():
  df = pd.read_csv('municipiosmg.csv')
  portais = df['Portal da Prefeitura']
  possible_url_array = []
  most_likely_url_array = []
  esq, dire = 0, 856

  for portal in portais[esq:dire]:
    possible_urls, most_likely_urls = get_url(portal)
    possible_url_array.append(possible_urls) 
    most_likely_url_array.append(most_likely_urls)  


  new_df = pd.DataFrame({'Cidades': df['Cidades'][esq:dire], 
                        'Portal da Prefeitura': df['Portal da Prefeitura'][esq:dire], 
                        'Possível Portal da Transparência': possible_url_array,
                        'Provável Portal da Transparência': most_likely_url_array})
  new_df.to_csv('portais9.csv')


main()
