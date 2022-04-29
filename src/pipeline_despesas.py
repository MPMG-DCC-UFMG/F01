import json
from validadores.despesas import empenhos
from validadores.despesas import pagamentos
from validadores.despesas import consulta_favorecido
from validadores.despesas import gerar_relatorio
from validadores.despesas import relatorios

# Siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb


def save_json(job_name, result):
    with open('results/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))


def pipeline_despesas(keywords, job_name):

    # Subtag - Empenhos
    validador_empenhos = empenhos.ValidadorEmpenhos(job_name, keywords['empenhos'])
    output_empenhos = validador_empenhos.predict()
    
    # Subtag - Pagamentos
    validador_pagamentos = pagamentos.ValidadorPagamentos(job_name, keywords['pagamentos'])
    output_pagamentos = validador_pagamentos.predict()

    # Subtag - Possibilita a consulta de empenhos ou pagamentos por favorecido	
    validador_consulta_favorecido = consulta_favorecido.ValidadorConsultaFavorecido(job_name, keywords['consulta_favorecido'])
    output_consulta_favorecido = validador_consulta_favorecido.predict()

    # Subtag - Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto	
    validador_gerar_relatorios = gerar_relatorio.ValidadorGerarRelatorios(job_name, keywords['gerar_relatorios'])
    output_gerar_relatorios = validador_gerar_relatorios.predict()

    # # Subtag - Relatórios
    validador_relatorios = relatorios.ValidadorRelatorios(job_name, keywords['relatorios'])
    output_relatorios = validador_relatorios.predict()

    try:
        with open('results/' + job_name + '.json') as fp:
            result = json.load(fp)
    except:
        result = {}

    result['27'] = output_empenhos['numero']['predict']
    result['28'] = output_empenhos['valor']['predict']
    result['29'] = output_empenhos['data']['predict']
    result['30'] = output_empenhos['favorecido']['predict']
    result['31'] = output_empenhos['descricao']['predict']

    result['32'] = output_pagamentos['valor']['predict']
    result['33'] = output_pagamentos['data']['predict']
    result['34'] = output_pagamentos['favorecido']['predict']
    result['35'] = output_pagamentos['empenho_de_referencia']['predict']

    result['36'] = output_consulta_favorecido['consulta_favorecido']['predict']   
    result['37'] = output_gerar_relatorios['gerar_relatorios']['predict']    

    print(result['27'],result['28'],result['29'],result['30'],result['31'])
    print(result['32'],result['33'],result['34'],result['35'])
    print(result['36'])
    print(result['37'])
    save_json(job_name, result)


jobs = municipios_siplanweb
keywords = keywords_siplanweb

for job_name in jobs:
    print(f"** {job_name} **")
    pipeline_despesas(keywords['despesas'], job_name)