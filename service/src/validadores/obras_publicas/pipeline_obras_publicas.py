from src.validadores.utils import handle_files
from src.validadores.obras_publicas.dados_para_acompanhamento import ValidadorDadosParaAcompanhamento

def pipeline_obras_publicas(keywords, job_name):
    try:
        keywords = keywords['obras_publicas']
    except KeyError:
        return None

    obras_publicas = {
        'dados_para_acompanhamento': {},
    }

    # Subtag - Dados para acompanhamento
    validador_dados_para_acompanhamento = ValidadorDadosParaAcompanhamento(job_name, keywords['dados_para_acompanhamento'])
    obras_publicas['dados_para_acompanhamento'] = validador_dados_para_acompanhamento.predict()

    return obras_publicas