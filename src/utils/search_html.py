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

def get_aria_labels (soup):

    #Get all tags and return a list with all aria_labels

    aria_labels =  [tag.get('aria-label') for tag in soup.find_all() if tag.get('aria-label') != None]
    return aria_labels

def search_tags_address(tags):
    address = [i for i in tags if ("endereco" in i) or ("address" in i)]
    return address

def count_matches (text, keyword_to_search):
    """
    Checa quantas ocorrrencias de uma palavra em um texto.

    Parameters
    ----------
    text: str
        String a ser verificada.
    keyword_to_search: string
        Palavra(s) a ser(em) procurada(s) no documento html.
        
    Returns
    -------
    int
        Número de vezes que a keyword_to_search foi encontrada no text.
    """

    matches = 0
    if type(keyword_to_search) is list:
        for i in keyword_to_search:
            matches += text.lower().count(i.lower())
    if type(keyword_to_search) is str:
        matches = text.lower().count(keyword_to_search.lower())

    return matches

def analyze_botoes(soup, keyword_to_search):
    """
    Retorna a quantidade de vezes que uma determinada palavra está presente em algum botão html.

    Parameters
    ----------
    soup: html
        String a ser verificada
    keyword_to_search: string
        Palavra a ser procurada nos botões
        
    Returns
    -------
    int
        Número de vezes que a keyword_to_search foi encontrada em botões.
    """
    num_matches = 0
    titles = get_tags_title(soup)
    for title in titles:
        num_matches += count_matches (title, keyword_to_search)
    return num_matches

def analyze_aria_label(soup, keyword_to_search):
    """
    Retorna a quantidade de vezes que uma determinada palavra está presente em atributo aria_label.

    Parameters
    ----------
    soup: html
        String a ser verificada
    keyword_to_search: string
        Palavra a ser procurada nos "aria_label"s
        
    Returns
    -------
    int
        Número de vezes que a keyword_to_search foi encontrada.
    """
    num_matches = 0
    titles = get_aria_labels(soup)
    for title in titles:
        num_matches += count_matches (title, keyword_to_search)
    return num_matches

def analyze_placeholders(soup, keyword_to_search):
    """
    Retorna a quantidade de vezes que uma determinada palavra está presente em algum placeholder html.

    Parameters
    ----------
    soup: html
        String a ser verificada
    keyword_to_search: string
        Palavra a ser procurada nos placeholders.
        
    Returns
    -------
    int
        Número de vezes que a keyword_to_search foi encontrada em placeholders.
    """
    num_matches = 0
    inputs = soup.find_all('input')
    for input in inputs:
        try:
            num_matches += count_matches (input['placeholder'], keyword_to_search)
        except KeyError:
            continue
    return num_matches

def analyze_html(html_files, keyword_to_search):

    """
    Checa quantas ocorrências existem em cada arquivo em: palavras no texto html, 
    no título de alguma tag, placeholder ou aria-label.

    Parameters
    ----------
    html_files: list
        Lista de arquivos html a serem verificados.
    keyword_to_search: list ou string
        Palavra ou lista de palavras a serem procuradas no documento html.
        
    Returns
    -------
    DataFrame
        Coluna 'files' com os arquivos verificados, 'matches' com a quanditade de ocorrência 
        das palavras e words com as palavras que ocorreram.
    """

    if type(keyword_to_search) is str:
        keyword_to_search = [keyword_to_search]

    matches = []
    words_matches = []

    result = pd.DataFrame({'files': html_files})

    for path in html_files:
        
        num_matches = 0
        words = []
        soup = read.read_html(path)

        if type(keyword_to_search) is list:

            for keyword in keyword_to_search:

                num_matches_keyword = 0

                # No texto
                num_matches_keyword += count_matches (soup.getText(), keyword)

                # No título de um botão
                num_matches_keyword += analyze_botoes (soup, keyword)

                # Em algum placeholder
                num_matches_keyword += analyze_placeholders (soup, keyword)

                # Em algum aria-label
                num_matches_keyword += analyze_aria_label (soup, keyword)

                if num_matches_keyword:
                    words.append(keyword)

                num_matches += num_matches_keyword

        matches.append(num_matches)
        words_matches.append(words)

    result = pd.DataFrame({'files': html_files, 'matches': matches, 'words':words_matches})

    return result

