from src.validadores.utils import handle_files
from src.validadores.despesas_com_diarias.despesas_com_diarias import ValidadorDespesasComDiarias

def pipeline_despesas_com_diarias(keywords, job_name):
    try:
        keywords = keywords['despesas_com_diarias']
    except KeyError:
        return None

    despesas_com_diarias = {
        'despesas_com_diarias': {},
    }

    # Subtag - Requisitos Exigios
    validador_despesas_com_diarias = ValidadorDespesasComDiarias(job_name, keywords['despesas_com_diarias'])
    despesas_com_diarias['despesas_com_diarias'] = validador_despesas_com_diarias.predict()

    return despesas_com_diarias