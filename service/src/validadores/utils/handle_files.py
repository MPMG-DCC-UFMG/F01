import os
import json
from pathlib import Path
from src.validadores.utils.path_functions import format_city_names

class ErroAoAbrirArquivo(Exception):
    def __init__(self, message, cause):
        super(ErroAoAbrirArquivo, self).__init__(message + u', causado por ' + str(cause))
        self.cause = cause

def get_keywords_do_template(template):
    """
    Obtem os parâmetro de um template.

    Parameters
    ----------
    template: String 
        Nome do arquivo com os parâmetro do template.
        
    Returns
    -------
    keywords: JSON
        JSON com os parâmetro do template.
    """
    try:
        with open(os.getcwd() + f"/src/empresa/parametros_templates/constants/{template}.json") as fp:
            parametros = json.load(fp)
    except FileNotFoundError as e:
        raise ErroAoAbrirArquivo(f"Erro ao abrir parâmetro {template}", e) from None
    else:
        return parametros

def abrir_existente(job_name):
    try:
        with open('results/' + job_name + '.json') as fp:
            result = json.load(fp)
    except:
        result = {}
    return result

def save_dict_in_json(job_name, result):
    with open('results/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))