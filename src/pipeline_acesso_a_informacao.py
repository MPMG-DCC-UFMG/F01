from utils import salvar_resultado
from validadores.acesso_a_informacao.requisitos_exigidos import ValidadorRequisitosExigidos

# Siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb

def pipeline_acesso_a_infomacao(keywords, job_name):

    # Subtag - Requisitos Exigios
    validador_requisitos_exigidos = ValidadorRequisitosExigidos(job_name, keywords['requisitos_exigidos'])
    output_requisitos_exigidos = validador_requisitos_exigidos.predict()

    result = salvar_resultado.abrir_existente(job_name)

    result['8'] = output_requisitos_exigidos['busca']['predict']  
    result['9'] = output_requisitos_exigidos['busca']['predict'] 
    result['10'] = output_requisitos_exigidos['busca']['predict'] 
    result['11'] = output_requisitos_exigidos['busca']['predict'] 
    result['12'] = output_requisitos_exigidos['busca']['predict'] 

    salvar_resultado.save_dict_in_json(job_name, result)

jobs = municipios_siplanweb
keywords = keywords_siplanweb

for job_name in jobs:
    print(f"** {job_name} **")
    pipeline_acesso_a_infomacao(keywords['acesso_a_informacoes'], job_name)