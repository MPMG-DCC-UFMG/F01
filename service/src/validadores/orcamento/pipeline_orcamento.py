from src.validadores.orcamento import legislacao
from src.validadores.orcamento import execucao


def pipeline_orcamento(keywords, job_name):
    try:
        keywords = keywords['orcamento']
    except KeyError:
        return None

    orcamento = {}

    # Subtag - Legislação
    validador_legislacao = legislacao.ValidadorLegislacao(job_name, keywords['legislacao'])
    orcamento['legislacao'] = validador_legislacao.predict()


    # Subtag - Execução
    validador_execucao = execucao.ValidadorExecucao(job_name, keywords['execucao'])
    orcamento['execucao'] = validador_execucao.predict()
    

    return orcamento