from utils import handle_files
from validadores.contratos.link_de_acesso import DadosDosContratos

def pipeline_contratos(keywords, job_name):

    # Subtag - Link de Acesso
    validador_link_de_acesso = DadosDosContratos(job_name, keywords['link_de_acesso'])
    output_link_de_acesso = validador_link_de_acesso.predict()

    result = handle_files.abrir_existente(job_name)
    # print(output_link_de_acesso)
    
    # Dados de Parcerias
    result['22'] = output_link_de_acesso['link_de_acesso']['predict']

    handle_files.save_dict_in_json(job_name, result)