from src.validadores.utils import handle_files
from src.validadores.acesso_a_informacao.informacoes import ValidadorInformacoes
from src.validadores.acesso_a_informacao.requisitos_exigidos import ValidadorRequisitosExigidos
from src.validadores.acesso_a_informacao.dados_abertos import ValidadorDadosAbertos

def pipeline_acesso_a_informacao(keywords, job_name):
    try:
        keywords = keywords['acesso_a_informacao']
    except KeyError:
        return None

    acesso_a_informacao = {
        'requisitos_exigidos': {},
        'bases_de_dados_abertos': {},
    }

    # # Subtag - Informações
    # validador_informacoes = ValidadorInformacoes(job_name, keywords['informacoes'])
    # acesso_a_informacao['informacoes'] = validador_informacoes.predict()

    # Subtag - Bases de dados abertos
    validador_dados_abertos = ValidadorDadosAbertos(job_name, keywords['dados_abertos'])
    acesso_a_informacao['bases_de_dados_abertos'] = validador_dados_abertos.predict()

    # Subtag - Requisitos Exigios
    # validador_requisitos_exigidos = ValidadorRequisitosExigidos(job_name, keywords['requisitos_exigidos'])
    # output_requisitos_exigidos = validador_requisitos_exigidos.predict()
    # handle_files.save_dict_in_json(job_name, result)

    return acesso_a_informacao

