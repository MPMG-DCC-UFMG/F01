from src.validadores.utils import handle_files
from src.validadores.receitas import dados_das_receitas

def pipeline_receitas(keywords, job_name):
    try:
        keywords = keywords['receitas']
    except KeyError:
        return None

    # Subtag - dados_das_receitas
    validador_dados_das_receitas = dados_das_receitas.ValidadorDadosDasReceitas(job_name, keywords['dados_das_receitas'])
    output_dados_das_receitas = validador_dados_das_receitas.predict()

    return output_dados_das_receitas