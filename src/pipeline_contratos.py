from utils import handle_files
from validadores.contratos.dados_dos_contratos import ValidadorDadosDosContratos
from validadores.contratos.conteudo_integral import ValidadorConteudoIntegral
from validadores.contratos.gerar_relatorio import ValidadorGerarRelatorio

def pipeline_contratos(keywords, job_name):

    # Subtag - Dados dos contratos
    validador_dados_dos_contratos = ValidadorDadosDosContratos(job_name, keywords['dados_dos_contratos'])
    output_dados_dos_contratos = validador_dados_dos_contratos.predict()

    # Subtag - Disponibiliza o conteúdo integral dos contratos
    validador_conteudo_integral = ValidadorConteudoIntegral(job_name, keywords['conteudo_integral'])
    output_conteudo_integral = validador_conteudo_integral.predict()

    # Permite gerar relatório da consulta de licitações ou de contratos em formato aberto	
    validador_gerar_relatorio = ValidadorGerarRelatorio(job_name, keywords['gerar_relatorio'])
    output_gerar_relatorio = validador_gerar_relatorio.predict()

    result = handle_files.abrir_existente(job_name)
    
    # Dados dos Contratos
    result['51'] = output_dados_dos_contratos['objeto']['predict']
    result['52'] = output_dados_dos_contratos['valor']['predict']
    result['53'] = output_dados_dos_contratos['favorecido']['predict']
    result['54'] = output_dados_dos_contratos['numero_ano_do_contrato']['predict']
    result['55'] = output_dados_dos_contratos['vigencia']['predict']
    result['56'] = output_dados_dos_contratos['licitacao_de_origem']['predict']

    # Disponibiliza o conteúdo integral dos contratos	
    result['57'] = output_conteudo_integral['conteudo_integral']['predict']

    # Permite gerar relatório da consulta de licitações ou de contratos em formato aberto	
    result['58'] = output_gerar_relatorio['gerar_relatorio']['predict']

    handle_files.save_dict_in_json(job_name, result)