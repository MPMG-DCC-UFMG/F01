from src.validadores.utils import handle_files
from src.validadores.licitacoes.processos_licitatorios import ValidadorProcessosLicitatorios
from src.validadores.licitacoes.registro_dos_procedimentos import ValidadorRegistroDosProcedimentos
from src.validadores.licitacoes.editais import ValidadorEditais
from src.validadores.licitacoes.resultado_das_licitacoes import ValidadorResultadosDasLicitacoes

def pipeline_licitacoes(keywords, job_name):
    try:
        keywords = keywords['licitacoes']
    except KeyError:
        return None

    licitacoes = {
        'processos_licitatorios': {},
        # 'registro_dos_procedimentos': {},
        # 'editais': {},
        # 'resultado_das_licitacoes': {}
    }

    # Subtag - Processos Licitatorios
    # validador_processos_licitatorios = ValidadorProcessosLicitatorios(job_name, keywords['processos_licitatorios'])
    # licitacoes['processos_licitatorios'] = validador_processos_licitatorios.predict()

    # Subtag - Registro dos procedimentos Inexibilidade e Dispensa
    # validador_registro_dos_procedimentos = ValidadorRegistroDosProcedimentos(job_name, keywords['registro_dos_procedimentos'])
    # licitacoes['processos_licitatorios'] = validador_registro_dos_procedimentos.predict()

    # Subtag Editais
    validador_editais = ValidadorEditais(job_name, keywords['editais'])
    licitacoes['editais'] = validador_editais.predict()

    # # Resultados das licitações
    # validador_resultado_das_licitacoes = ValidadorResultadosDasLicitacoes(job_name, keywords['resultado_das_licitacoes'])
    # licitacoes['resultado_das_licitacoes'] = validador_resultado_das_licitacoes.predict()

    return licitacoes