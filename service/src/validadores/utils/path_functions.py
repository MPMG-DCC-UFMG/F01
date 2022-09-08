import os
from pathlib import Path
import codecs
from errors import FileDescriptionVazio

def agg_paths_by_type(paths):

    files = {'csv': [], 'xls': [], 'html': [], 'pdf': [], 'doc':[], 'bat':[], 'no_suffix':[]}

    for path in paths:
        
        try:
            suffix = Path(path).suffixes[0]

            if suffix == ".xls":
                files['xls'].append(path)
            elif suffix == '.csv':
                files['csv'].append(path)
            elif suffix == '.bat':
                files['bat'].append(path)   
            elif (suffix == ".html") or (suffix == '.xml'):
                files['html'].append(path)
            elif (suffix == ".pdf"):
                files['pdf'].append(path)
            elif (suffix == ".doc") or (suffix == '.docx'):
                files['doc'].append(path)

        except IndexError:
            files['no_suffix'].append(path)

    return files


def format_path(path):
    path = path.split(os.sep)
    return os.sep.join(path[: len(path)-1])
    
def get_extension(path):
    return path.split('.')[-1]

def get_name(path):
    return path.split('/')[-1]

def filter_paths(paths, words):
    """
    Filtra os caminhos retornados pelo indexador por palavras-chave
    """

    filtered_paths = []
    for i in paths:
        if type(words) is list:
            for word in words:
                if i.find(word) != -1:
                    filtered_paths.append(i)
                    break
        else:
            if i.find(words) != -1:
                filtered_paths.append(i)

                
    return filtered_paths

def preprocess_paths(sorted_result, word):

    paths = (sorted(set(sorted_result)))
    print('preprocess_paths', paths)
    # paths = filter_paths(paths, word)


    return paths

def create_valid_path (html_files, path_base, pattern='/tmp/es/data'):

    return [i.replace(pattern, path_base) for i in html_files]


def get_url(filename):
    """
    Fornece a url do arquivo através do "file_description", descrição dos arquivos coletados.

    Parameters
    ----------
    filename: string
        Caminho para o arquivo a ser analisado
        
    Returns
    -------
    url: string
       Url do arquivo.
    """

    file_description = format_path(filename) + "/" + 'file_description.jsonl'
    
    try:
        arquivo = codecs.open(file_description, 'r', 'utf-8').readlines()
        if len(arquivo) == 0:
            raise FileDescriptionVazio

        for line in arquivo:
            json = eval(line)
            if (json['file_name'] == get_name(filename)):
                return json['url']
    
    except FileDescriptionVazio:
        print(f"Warning: File_description em {file_description} vazio ")
        return filename


def format_city_names(municipipos):
    ori = "ãâáíẽéêóôõçú "
    rep  = "aaaioeeooocu_"
    result = []
    for municipio in municipipos:
        new = municipio.lower()
        for i in range(len(ori)):
            if ori[i] in new:
                new = new.replace(ori[i],rep[i])
        result.append(new)
    return result

def list_files(diretorio):
    """
    Fornece a lista de caminhos absolutos para todos os arquvos em um diretório.

    Parameters
    ----------
    diretorio: pathlib.PosixPath 
        Diretório que sera analisado
        
    Returns
    -------
    paths: List of string
       Lista de caminhos absolutos para todos os arquivos em um diretório.
    """
    paths = []
    
    for p, _, files in os.walk(diretorio):
        for file_ in files:
            paths.append(os.path.join(p, file_))

    return paths