import json
from utils.path_functions import format_city_names

class ErroAoAbrirArquivo(Exception):
    def __init__(self, message, cause):
        super(ErroAoAbrirArquivo, self).__init__(message + u', causado por ' + str(cause))
        self.cause = cause

def get_municipios_do_template(template):
    """
    Abre o arquivo de municipios de um template e retorna os seus municípios.

    Parameters
    ----------
    template: String 
        Nome do arquivo com os parâmetro do template.
        
    Returns
    -------
    municipios: List
        Lista com o nome de cada municipio formatado sem acento e com espaço substituido por "_".
    """
    try:
        with open(f"src/parametros_templates/municipios/{template}.json") as fp:
            list_municipios = json.load(fp)
    except:
        print(f"Erro ao abrir lista de município do template - {template}")
        return

    municipios = format_city_names(list_municipios)
    return municipios

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
        with open(f"src/parametros_templates/constants/{template}.json") as fp:
            parametros = json.load(fp)
    except FileNotFoundError as e:
        raise ErroAoAbrirArquivo(f"Erro ao abrir parâmetro {template}", e) from None
    else:
        return parametros

def abrir_existente(job_name):
    try:
        with open('resultados/' + job_name + '.json') as fp:
            result = json.load(fp)
    except:
        result = {}
    return result

def save_dict_in_json(job_name, result):
    with open('resultados/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))