from utils import indexing
from utils import path_functions
from utils import salvar_resultado

from validadores import licitacoes 

num_matches = 1000 

def pipeline_licitacoes(keywords, job_name):

    try:
        types = keywords['types']
    except KeyError:
        types = 'html'

    search_term = keywords['search_term']
    keywords_to_search = keywords['keywords']
    proc_lic_itens = keywords['proc_lic_itens']
    editais = keywords['editais']

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
    validador = licitacoes.ValidadorLicitacoes(files, proc_lic_itens[0], ttype=types)
    # print(len(validador.files['bat']))

    # Procedimentos Licitatórios número
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[0])
    result_explain = validador.explain(result, proc_lic_itens[0])
    output['proc_lic_numero']['predict'] = isvalid
    output['proc_lic_numero']['explain'] = result_explain
    
    # Procedimentos Licitatórios modalidade
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[1])
    result_explain = validador.explain(result, proc_lic_itens[1])
    output['proc_lic_modalidade']['predict'] = isvalid
    output['proc_lic_modalidade']['explain'] = result_explain

    # Procedimentos Licitatórios objeto
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[2])
    result_explain = validador.explain(result, proc_lic_itens[2])
    output['proc_lic_objeto']['predict'] = isvalid
    output['proc_lic_objeto']['explain'] = result_explain

    # Procedimentos Licitatórios status
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[3])
    result_explain = validador.explain(result, proc_lic_itens[3])
    output['proc_lic_status']['predict'] = isvalid
    output['proc_lic_status']['explain'] = result_explain

    # Procedimentos Licitatórios resultado
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[4])
    result_explain = validador.explain(result, proc_lic_itens[4])
    output['proc_lic_resultado']['predict'] = isvalid
    output['proc_lic_resultado']['explain'] = result_explain

    # Procedimentos modalidade Inexigibilidade e Dispensa
    isvalid_inexigibilidade, result_inexigibilidade = validador.predict_inexibilidade()
    isvalid_dispensa, result_dispensa = validador.predict_dispensa()
    isvalid = isvalid_inexigibilidade and isvalid_dispensa 
    result = result_inexigibilidade['inexigibilidade']
    result.extend(result_dispensa['dispensa'])
    result = {'inexigibilidade e dispensa': result} 
    result_explain = validador.explain(result, 'inexigibilidade e dispensa')
    output['inexigibilidade_e_dispensa']['predict'] = isvalid
    output['inexigibilidade_e_dispensa']['explain'] = result_explain

    # Disponibilização de Editais
    isvalid, result = validador.predict_editais(editais)
    result_explain=validador.explain(result, 'editais')
    output['editais']['predict'] = isvalid
    output['editais']['explain'] = result_explain

    # Permite Busca
    isvalid, result = validador.predict_busca()
    result_explain=validador.explain(result, 'busca')
    output['busca']['predict'] = isvalid
    output['busca']['explain'] = result_explain

    print(output)

    result = salvar_resultado.abrir_existente(job_name)
    
    # Processos licitatórios
    result['43'] = output['proc_lic_numero']['predict']
    result['44'] = output['proc_lic_modalidade']['predict']
    result['45'] = output['proc_lic_objeto']['predict']
    result['46'] = output['proc_lic_status']['predict']
    result['47'] = output['proc_lic_resultado']['predict']

    # Registro dos procedimentos
    result['48'] = output['inexigibilidade_e_dispensa']['predict']

    # Editais
    result['49'] = output['editais']['predict']

    # Resultados das licitações 
    result['50'] = output['busca']['predict']

    salvar_resultado.save_dict_in_json(job_name, result)