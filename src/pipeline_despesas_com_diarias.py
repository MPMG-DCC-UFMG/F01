from utils import handle_files
from validadores.despesas_com_diarias.despesas_com_diarias import ValidadorDespesasComDiarias

# Siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb

def pipeline_despesas_com_diarias(keywords, job_name):

    # Subtag - Requisitos Exigios
    validador_despesas_com_diarias = ValidadorDespesasComDiarias(job_name, keywords['despesas_com_diarias'])
    output_despesas_com_diarias = validador_despesas_com_diarias.predict()

    result = handle_files.abrir_existente(job_name)

    result['111'] = output_despesas_com_diarias['nome']['predict']  
    result['112'] = output_despesas_com_diarias['cargo_funcao']['predict']  
    result['113'] = output_despesas_com_diarias['valores_recebidos']['predict']  
    result['114'] = output_despesas_com_diarias['periodo_da_viagem']['predict']  
    result['115'] = output_despesas_com_diarias['destino_da_viagem']['predict']
    result['116'] = output_despesas_com_diarias['motivo_da_viagem']['predict']
    result['117'] = output_despesas_com_diarias['numero_de_diarias']['predict']


    handle_files.save_dict_in_json(job_name, result)
    print(result['111'], result['112'], result['113'],result['114'],result['115'],result['116'], result['117'])

jobs = municipios_siplanweb
keywords = keywords_siplanweb

for job_name in jobs:
    print(f"** {job_name} **")
    pipeline_despesas_com_diarias(keywords['despesas_com_diarias'], job_name)