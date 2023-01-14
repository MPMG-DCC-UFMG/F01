from src.validadores.despesas import empenhos
from src.validadores.despesas import pagamentos
from src.validadores.despesas import relatorios
from src.validadores.despesas import gerar_relatorio
from src.validadores.despesas import consulta_favorecido

def pipeline_despesas(keywords, job_name):
    try:
        keywords = keywords['despesas']
    except KeyError:
        return None

    despesas = {
        'empenhos': {},
        'pagamentos': {},
        'consulta_favorecido': {},
        'gerar_relatorios': {},
        'relatorios': {}
    }

    # # Subtag - Empenhos
    # validador_empenhos = empenhos.ValidadorEmpenhos(job_name, keywords['empenhos'])
    # despesas['empenhos'] = validador_empenhos.predict()
    
    # # Subtag - Pagamentos
    # validador_pagamentos = pagamentos.ValidadorPagamentos(job_name, keywords['pagamentos'])
    # despesas['pagamentos'] = validador_pagamentos.predict()

    # # Subtag - Possibilita a consulta de empenhos ou pagamentos por favorecido	
    # validador_consulta_favorecido = consulta_favorecido.ValidadorConsultaFavorecido(job_name, keywords['consulta_favorecido'])
    # despesas['consulta_favorecido'] = validador_consulta_favorecido.predict()

    # # Subtag - Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto	
    # validador_gerar_relatorios = gerar_relatorio.ValidadorGerarRelatorios(job_name, keywords['gerar_relatorios'])
    # despesas['gerar_relatorios'] = validador_gerar_relatorios.predict()

    # # Subtag - Relatórios
    validador_relatorios = relatorios.ValidadorRelatorios(job_name, keywords['relatorios'])
    despesas['relatorios'] = validador_relatorios.predict()

    return despesas
