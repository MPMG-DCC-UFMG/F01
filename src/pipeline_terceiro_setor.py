from utils import handle_files
from validadores.terceiro_setor import dados_de_parcerias
from validadores.terceiro_setor import repasses

def pipeline_terceiro_setor(keywords, job_name):

    # Subtag - Dados de Parcerias
    validador_dados_de_parceria = dados_de_parcerias.ValidadorDadosDeParcerias(job_name, keywords['dados_de_parcerias'])
    output_dados_de_parceria = validador_dados_de_parceria.predict()
    print(output_dados_de_parceria)



    # # Subtag - Repasses
    # validador_repasses = repasses.ValidadorRepasses(job_name, keywords['repasses'])
    # output_repasses = validador_repasses.predict()

    # result = handle_files.abrir_existente(job_name)
    
    # # Dados de Parcerias
    # result['43'] = output_dados_de_parceria['data_de_celebração']['predict']
    # result['44'] = output_dados_de_parceria['objeto']['predict']
    # result['45'] = output_dados_de_parceria['conveniados']['predict']
    # result['46'] = output_dados_de_parceria['aditivos']['predict']

    # # Repasses
    # result['63'] = output_repasses['origem']['predict']
    # result['64'] = output_repasses['valor']['predict']
    # result['65'] = output_repasses['data']['predict']

    # handle_files.save_dict_in_json(job_name, result)