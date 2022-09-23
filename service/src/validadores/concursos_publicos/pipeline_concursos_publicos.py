from src.validadores.concursos_publicos.dados_do_concurso import ValidadorDadosDoConcurso
from src.validadores.concursos_publicos.copia_do_edital_do_concurso import ValidadorCopiaDoEdital
from src.validadores.concursos_publicos.divulgacao import ValidadorDivulgacaoRecursosDecisoes	

def pipeline_concursos_publicos(keywords, job_name):
    try:
        keywords = keywords['concursos_publicos']
    except KeyError:
        return None
    
    concursos_publicos = {
        'dados_do_concurso': {},
        'copia_do_edital_do_concurso': {},
        'divulgacao': {},
    }

    # Subtag - Dados dos Concursos
    validador_dados_do_concurso = ValidadorDadosDoConcurso(job_name, keywords['dados_do_concurso'])
    concursos_publicos['dados_do_concurso'] = validador_dados_do_concurso.predict()

    # Subtag - Cópia do edital do concurso	
    validador_copia_do_edital_do_concurso = ValidadorCopiaDoEdital(job_name, keywords['copia_do_edital_do_concurso'])
    concursos_publicos['copia_do_edital_do_concurso'] = validador_copia_do_edital_do_concurso.predict()

    # # Subtag - Divulgação dos recursos e respectivas decisões		
    validador_divulgacao = ValidadorDivulgacaoRecursosDecisoes(job_name, keywords['divulgacao_dos_recursos_e_respectivas_decisoes'])
    concursos_publicos['divulgacao'] = validador_divulgacao.predict()

    return concursos_publicos