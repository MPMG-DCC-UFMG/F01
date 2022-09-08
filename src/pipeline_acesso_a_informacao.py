from utils import handle_files
from validadores.acesso_a_informacao.informacoes import ValidadorInformacoes
from validadores.acesso_a_informacao.requisitos_exigidos import ValidadorRequisitosExigidos

def pipeline_acesso_a_informacao(keywords, job_name):

    # Subtag - Informações
    validador_requisitos_exigidos = ValidadorInformacoes(job_name, keywords['informacoes'])
    output_requisitos_exigidos = validador_requisitos_exigidos.predict()
    print(output_requisitos_exigidos)

    # Subtag - Requisitos Exigios
    # validador_requisitos_exigidos = ValidadorRequisitosExigidos(job_name, keywords['requisitos_exigidos'])
    # output_requisitos_exigidos = validador_requisitos_exigidos.predict()

    # result = handle_files.abrir_existente(job_name)

    # result['8'] = output_requisitos_exigidos['busca']['predict']  
    # result['9'] = output_requisitos_exigidos['exportar_relatorios']['predict'] 
    # result['10'] = output_requisitos_exigidos['info_atualizadas']['predict'] 
    # result['11'] = output_requisitos_exigidos['contato']['predict'] 
    # result['12'] = output_requisitos_exigidos['acessibilidade']['predict'] 

    # handle_files.save_dict_in_json(job_name, result)

