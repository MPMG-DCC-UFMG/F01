from utils import indexing
from utils import path_functions
from classifiers.despesas import empenhos

# Siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb

from classifiers import licitacoes 


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


def pipeline_licitacoes(keywords, num_matches, job_name):

    try:
        types = keywords['types']
    except KeyError:
        types = 'html'

    search_term = keywords['licitacoes']['search_term']
    keywords_to_search = keywords['licitacoes']['keywords']
    proc_lic_itens = keywords['licitacoes']['proc_lic_itens']
    editais = keywords['licitacoes']['editais']

    output = {
            'proc_lic_numero': {},
            'proc_lic_modalidade': {},
            'proc_lic_objeto': {},
            'proc_lic_status': {},
            'proc_lic_resultado': {},
            'inexigibilidade_e_dispensa': {},
            'editais': {},
            'busca': {}
            }

    #Search
    files = indexing.get_files(
        search_term, num_matches,
        job_name, keywords_search=keywords_to_search)
    
    files = path_functions.filter_paths(files, words=['licitacao','licitacoes'])
    files = path_functions.agg_paths_by_type(files)
    # print('bat', len(files['bat']))
    # print('pdf', len(files['pdf']))
    validador = licitacoes.Licitacoes(files, proc_lic_itens[0], ttype=types)
    # print(len(validador.files['bat']))

    # Procedimentos Licitatórios número
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[0])
    result_explain = licitacoes.explain(result, proc_lic_itens[0])
    output = add_in_dict(output, 'proc_lic_numero', isvalid, result_explain)
    
    # Procedimentos Licitatórios modalidade
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[1])
    result_explain = licitacoes.explain(result, proc_lic_itens[1])
    output = add_in_dict(output, 'proc_lic_modalidade', isvalid, result_explain)

    # Procedimentos Licitatórios objeto
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[2])
    result_explain = licitacoes.explain(result, proc_lic_itens[2])
    output = add_in_dict(output, 'proc_lic_objeto', isvalid, result_explain)

    # Procedimentos Licitatórios status
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[3])
    result_explain = licitacoes.explain(result, proc_lic_itens[3])
    output = add_in_dict(output, 'proc_lic_status', isvalid, result_explain)

    # Procedimentos Licitatórios resultado
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[4])
    result_explain = licitacoes.explain(result, proc_lic_itens[4])
    output = add_in_dict(output, 'proc_lic_resultado', isvalid, result_explain)

    # # Procedimentos modalidade Inexigibilidade e Dispensa
    isvalid_inexigibilidade, result_inexigibilidade = validador.predict_inexibilidade()
    isvalid_dispensa, result_dispensa = validador.predict_dispensa()
    isvalid = isvalid_inexigibilidade and isvalid_dispensa 
    result = result_inexigibilidade['inexigibilidade']
    result.extend(result_dispensa['dispensa'])
    result = {'inexigibilidade e dispensa': result} 
    result_explain = licitacoes.explain(result, 'inexigibilidade e dispensa')
    output = add_in_dict(output, 'inexigibilidade_e_dispensa', isvalid, result_explain)

    # # Disponibilização de Editais
    isvalid, result = validador.predict_editais(editais)
    result_explain=licitacoes.explain(result, 'editais')
    output = add_in_dict(output, 'editais', isvalid, result_explain)

    # # Permite Busca
    isvalid, result = validador.predict_busca()
    result_explain=licitacoes.explain(result, 'busca')
    output = add_in_dict(output, 'busca', isvalid, result_explain)

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

    result['43'] = output['proc_lic_numero']['predict']
    result['44'] = output['proc_lic_modalidade']['predict']
    result['45'] = output['proc_lic_objeto']['predict']
    result['46'] = output['proc_lic_status']['predict']
    result['47'] = output['proc_lic_resultado']['predict']
    result['48'] = output['inexigibilidade_e_dispensa']['predict']
    result['49'] = output['editais']['predict']
    result['50'] = output['busca']['predict']

    save_json(job_name, result)


num_matches = 1000
jobs = municipios_siplanweb
keywords = keywords_siplanweb

for job_name in jobs:
    pipeline_licitacoes(keywords, num_matches, job_name)