from src.validadores.utils import handle_files
from src.validadores.acesso_a_informacao.informacoes import ValidadorInformacoes
from src.validadores.acesso_a_informacao.requisitos_exigidos import ValidadorRequisitosExigidos

def pipeline_acesso_a_informacao(keywords, job_name):
    try:
        keywords = keywords['acesso_a_informacao']
    except KeyError:
        return None

    acesso_a_informacao = {
        'requisitos_exigidos': {},
    }

    # Subtag - Informações
    validador_informacoes = ValidadorInformacoes(job_name, keywords['informacoes'])
    acesso_a_informacao['informacoes'] = validador_informacoes.predict()

    # Subtag - Requisitos Exigios
    # validador_requisitos_exigidos = ValidadorRequisitosExigidos(job_name, keywords['requisitos_exigidos'])
    # output_requisitos_exigidos = validador_requisitos_exigidos.predict()
    # handle_files.save_dict_in_json(job_name, result)

    return acesso_a_informacao

