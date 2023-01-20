from src.validadores.utils import handle_files
from src.validadores.contratos.dados_dos_contratos import ValidadorDadosDosContratos
from src.validadores.contratos.conteudo_integral import ValidadorConteudoIntegral
from src.validadores.contratos.gerar_relatorio import ValidadorGerarRelatorio

def pipeline_contratos(keywords, job_name):
    try:
        keywords = keywords['contratos']
    except KeyError:
        return None

    contratos = {
        'dados_dos_contratos': {},
        'conteudo_integral': {},
        'gerar_relatorio': {}
    }

    # Subtag - Dados dos contratos
    validador_dados_dos_contratos = ValidadorDadosDosContratos(job_name, keywords['dados_dos_contratos'])
    contratos['dados_dos_contratos'] = validador_dados_dos_contratos.predict()

    # Subtag - Disponibiliza o conteúdo integral dos contratos
    validador_conteudo_integral = ValidadorConteudoIntegral(job_name, keywords['conteudo_integral'])
    contratos['conteudo_integral'] = validador_conteudo_integral.predict()

    # Permite gerar relatório da consulta de licitações ou de contratos em formato aberto	
    validador_gerar_relatorio = ValidadorGerarRelatorio(job_name, keywords['gerar_relatorio'])
    contratos['gerar_relatorio'] = validador_gerar_relatorio.predict()

    return contratos
