import os
from pathlib import Path
import codecs

def agg_paths_by_type(paths):

    files = {'csv': [], 'xls': [], 'html': [], 'pdf': [], 'doc':[]}

    for path in paths:

        suffix = Path(path).suffixes[0]

        if suffix == ".xls":
            files['xls'].append(path)
        elif suffix == '.csv':
            files['csv'].append(path)
        elif (suffix == ".html") or (suffix == '.xml'):
            files['html'].append(path)
        elif (suffix == ".pdf"):
            files['pdf'].append(path)
        elif (suffix == ".doc") or (suffix == '.docx'):
            files['doc'].append(path)

    return files


def format_path(path):
    path = path.split(os.sep)
    return os.sep.join(path[3: len(path)-1])
    
def get_extension(path):
    return path.split('.')[-1]

def get_name(path):
    return path.split('/')[-1]

def get_paths(indexes):

    paths = []

    for i in indexes:
        extensions = get_extension(str(i[2]))
        path = format_path (str(i[2]))
        paths.append((path, extensions))

    return paths

def format_path(path):
    path = path.split(os.sep)
    return os.sep.join(path[3: len(path)-1])

def filter_paths(paths, word):
    """
    Filtra os caminhos retornados pelo indexador por uma palavra-chave
    """

    filtered_paths = []
    for i in paths:
        if i[0].find(word) != -1:
            filtered_paths.append(i)
            
    return filtered_paths

def filter_paths2(paths, words):
    """
    Filtra os caminhos retornados pelo indexador por palavras-chave
    """

    filtered_paths = []
    for i in paths:
        for word in words:
            if i.find(word) != -1:
                filtered_paths.append(i)
                break
            
    return filtered_paths

def preprocess_paths(sorted_result, word):

    paths = get_paths(sorted_result)
    paths = (sorted(set(paths)))
    paths = filter_paths(paths, word)

    return paths

def create_valid_path (html_files, path_base, pattern='/tmp/es/data'):

    return [i.replace(pattern, path_base) for i in html_files]


def get_url(path_base, filename):

    file_description = path_base + "/" + format_path(filename) + "/" + 'file_description.jsonl'
    arquivo = codecs.open(file_description, 'r', 'utf-8').readlines()
    for line in arquivo:
        json = eval(line)
        if (json['file_name'] == get_name(filename)):
            return json['url']
