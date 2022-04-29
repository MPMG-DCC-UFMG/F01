import itertools
from utils import read
import pandas as pd

def get_tags_id (soup):

    #Get all tags id and return a list with all ids
    tags_id = [tag.get('id') for tag in soup.find_all() if tag.get('id') != None]

    return tags_id

def get_tags_class (soup):

    #Get all tags class and return a list with all class
    tags_class =  [tag.get('class') for tag in soup.find_all() if tag.get('class') != None]
    print(tags_class)
    tags_class = list(itertools.chain(*tags_class))
    
    return tags_class

def get_tags_title (soup):

    #Get all tags class and return a list with all class
    title_class =  [tag.get('title') for tag in soup.find_all() if tag.get('title') != None]
    return title_class

def search_tags_address(tags):
    address = [i for i in tags if ("endereco" in i) or ("address" in i)]
    return address

def count_matches (text, keyword_to_search):
    """
    Checa quantas ocorrrencias de uma palavra em um texto

    Parameters
    ----------
    text: str
        String a ser verificada
    keyword_to_search: string
        Palavra a ser procuradas no documento html
        
    Returns
    -------
    int
        Número de vezes que a keyword_to_search foi encontrada no text
    """

    matches = 0
    if type(keyword_to_search) is list:
        for i in keyword_to_search:
            matches += text.lower().count(i.lower())
    if type(keyword_to_search) is str:
        matches = text.lower().count(keyword_to_search.lower())

    return matches

def analyze_html(html_files, keyword_to_search):

    """
    Checa quantas ocorrências existem de palavras no texto html ou no título de alguma tag de cada arquivo

    Parameters
    ----------
    html_files: list
        Lista de arquivos html a serem verificados
    keyword_to_search: list ou string
        Palavra ou lista de palavras a serem procuradas no documento html
        
    Returns
    -------
    DataFrame
        Coluna 'files' com os arquivos verificados e 'matches' com a quanditade de ocorrência das palavras
    """

    matches = []

    for path in html_files:
        
        # No texto
        soup = read.read_html(path)
        num_matches = count_matches (soup.getText(), keyword_to_search)

        # No título de um botão
        titles = get_tags_title(soup)
        for title in titles:
            num_matches += count_matches (title, keyword_to_search)
        matches.append(num_matches)

    result = pd.DataFrame({'files': html_files, 'matches': matches})

    return result
