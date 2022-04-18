from utils import indexing
from utils import path_functions
from validadores.despesas import empenhos
from validadores.despesas import pagamentos

# Siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb

"""
SAIR DAQUI
"""
import json

def save_json(job_name, result):
    with open('results/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))

def add_in_dict(output, item, isvalid, result_explain):
    output[item]['predict'] = isvalid
    output[item]['explain'] = result_explain
    return output

"""
SAIR DAQUI
"""

def pipeline_despesas(keywords, num_matches, job_name):

    output = {
            'empenhos_numero': {},
            'empenhos_valor': {},
            'empenhos_data': {},
            'empenhos_favorecido': {},
            'empenhos_descricao': {},
            'pagamentos_valor': {},
            'pagamentos_data': {},
            'pagamentos_favorecido': {},
            'pagamentos_empenho_de_referencia': {},
            'consulta': {},
            'relatorio': {},
            }

    #Serch files
    search_term = keywords['search_term']
    keywords_to_search = keywords['keywords_to_search']
    files = indexing.get_files(search_term, num_matches, job_name, keywords_search=keywords_to_search)

    # Filter /despesas
    files_empenhos = path_functions.filter_paths(files, words=['empenhos'])

    # Subtag - Empenhos
    keywords_empenhos = keywords['empenhos']
    validador_empenhos = empenhos.Empenhos(files_empenhos, ttype=['html','bat'])

    # Item - Empenhos - Número
    keyword_numero = keywords_empenhos['numero']
    isvalid, result = validador_empenhos.predict_numero(keyword_numero)
    explain = validador_empenhos.explain(result, keyword_numero, 'o número')
    output = add_in_dict(output, 'empenhos_numero', isvalid, explain)

    # Item - Empenhos - Valor
    keyword_valor = keywords_empenhos['valor']
    isvalid, result = validador_empenhos.predict_valor(keyword_valor)
    explain = validador_empenhos.explain(result, keyword_valor, 'o valor')
    output = add_in_dict(output, 'empenhos_valor', isvalid, explain)

    # Item - Empenhos - Data
    keyword_data = keywords_empenhos['data']
    isvalid, result = validador_empenhos.predict_data(keyword_data)
    explain = validador_empenhos.explain(result, keyword_data, 'a data')
    output = add_in_dict(output, 'empenhos_data', isvalid, explain)

    # Item - Empenhos - Favorecido
    keyword_favorecido = keywords_empenhos['favorecido']
    isvalid, result = validador_empenhos.predict_favorecido(keyword_favorecido)
    explain = validador_empenhos.explain(result, keyword_favorecido, 'o favorecido')
    output = add_in_dict(output, 'empenhos_favorecido', isvalid, explain)

    # Item - Empenhos - Descrição
    keyword_descricao = keywords_empenhos['descricao']
    isvalid, result = validador_empenhos.predict_descricao(keyword_descricao)
    explain = validador_empenhos.explain(result, keyword_descricao, 'a descrição')
    output = add_in_dict(output, 'empenhos_descricao', isvalid, explain)

    
    # Subtag - Empenhos
    keywords_pagamentos = keywords['pagamentos']
    validador_pagamentos = pagamentos.ValidadorPagamentos(job_name, keywords_pagamentos)
    output_pagamentos = validador_pagamentos.predict()


    """
    REFATORAR
    """

    try:
        with open('results/' + job_name + '.json') as fp:
            result = json.load(fp)
    except:
        result = {}


    """
    REFATORAR
    """    
    
    result['26'] = output['empenhos_numero']['predict']
    result['27'] = output['empenhos_valor']['predict']
    result['28'] = output['empenhos_data']['predict']
    result['29'] = output['empenhos_favorecido']['predict']
    result['30'] = output['empenhos_descricao']['predict']

    result['31'] = output_pagamentos['pagamentos_valor']['predict']
    result['32'] = output_pagamentos['pagamentos_data']['predict']
    result['32'] = output_pagamentos['pagamentos_favorecido']['predict']
    result['33'] = output_pagamentos['pagamentos_empenho_de_referencia']['predict']

    print(result)
    save_json(job_name, result)


num_matches = 1000
jobs = municipios_siplanweb
keywords = keywords_siplanweb

for job_name in jobs:
    pipeline_despesas(keywords['despesas'], num_matches, job_name)