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
    tags_class = list(itertools.chain(*tags_class))
    
    return tags_class

def search_tags_address(tags):

    address = [i for i in tags if ("endereco" in i) or ("address" in i)]

    return address


def count_matches (text, keyword_to_search):

    matches = 0
    for i in keyword_to_search:
        matches += text.lower().count(i.lower())

    return matches

def analyze_html(html_files, keyword_to_search):

    matches = []

    for path in html_files:
        
        text = read.read_file(path)
        # print(path_functions.get_url("/home/asafe", path), count_matches (text, keyword_to_search))
        matches.append(count_matches (text, keyword_to_search))
        print(count_matches (text, keyword_to_search))

    result = pd.DataFrame({'files': html_files, 'matches': matches})

    return result
