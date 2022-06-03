from utils import salvar_resultado
from validadores.licitacoes import processos_licitatorios

# num_matches = 1000 

def pipeline_licitacoes(keywords, job_name):


    # Subtag - Processos Licitatorios
    validador_processos_licitatorios = processos_licitatorios.ValidadorProcessosLicitatorios(job_name, keywords['processos_licitatorios'])
    output_processos_licitatorios = validador_processos_licitatorios.predict()
    print(output_processos_licitatorios)    

    result = salvar_resultado.abrir_existente(job_name)
    
    # Processos licitatórios
    result['43'] = output_processos_licitatorios['numero']['predict']
    result['44'] = output_processos_licitatorios['modalidade']['predict']
    result['45'] = output_processos_licitatorios['objeto']['predict']
    result['46'] = output_processos_licitatorios['status']['predict']
    result['47'] = output_processos_licitatorios['resultado']['predict']

    # # Registro dos procedimentos
    # result['48'] = output['inexigibilidade_e_dispensa']['predict']

    # # Editais
    # result['49'] = output['editais']['predict']

    # # Resultados das licitações 
    # result['50'] = output['busca']['predict']

    salvar_resultado.save_dict_in_json(job_name, result)


    # try:
    #     types = keywords['types']
    # except KeyError:
    #     types = 'html'

    # output = {
    #         'inexigibilidade_e_dispensa': {},
    #         'editais': {},
    #         'busca': {}
    #         }
    
    #Search
    # files = indexing.get_files(
    #     search_term, num_matches,
    #     job_name, keywords_search=keywords_to_search)
    
    # files = path_functions.filter_paths(files, words=['licitacao','licitacoes'])
    # files = path_functions.agg_paths_by_type(files)
    # print('bat', len(files['bat']))
    # print('pdf', len(files['pdf']))
    # validador = licitacoes.ValidadorLicitacoes(files, proc_lic_itens[0], ttype=types)
    # print(len(validador.files['bat']))


    # # Procedimentos modalidade Inexigibilidade e Dispensa
    # isvalid_inexigibilidade, result_inexigibilidade = validador.predict_inexibilidade()
    # isvalid_dispensa, result_dispensa = validador.predict_dispensa()
    # isvalid = isvalid_inexigibilidade and isvalid_dispensa 
    # result = result_inexigibilidade['inexigibilidade']
    # result.extend(result_dispensa['dispensa'])
    # result = {'inexigibilidade e dispensa': result} 
    # result_explain = validador.explain(result, 'inexigibilidade e dispensa')
    # output['inexigibilidade_e_dispensa']['predict'] = isvalid
    # output['inexigibilidade_e_dispensa']['explain'] = result_explain

    # # Disponibilização de Editais
    # isvalid, result = validador.predict_editais(editais)
    # result_explain=validador.explain(result, 'editais')
    # output['editais']['predict'] = isvalid
    # output['editais']['explain'] = result_explain

    # # Permite Busca
    # isvalid, result = validador.predict_busca()
    # result_explain=validador.explain(result, 'busca')
    # output['busca']['predict'] = isvalid
    # output['busca']['explain'] = result_explain

    # print(output)

