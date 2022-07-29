from utils import handle_files
from validadores.servidores.dados_dos_servidores import ValidadorDadosDosServidores
from validadores.servidores.registro_da_remuneracao import ValidadorRegistroDaRemuneracao
from validadores.servidores.registro_por_lotacao import ValidadorRegistroPorLotacao
from validadores.servidores.auxilios import ValidadorAuxilios
from validadores.servidores.proventos_de_aposentadoria import ValidadorProventosDeAposentadoria
from validadores.servidores.proventos_de_pensao import ValidadorProventosDePensao
from validadores.servidores.relatorio_mensal import ValidadorRelatorioMensal
from validadores.servidores.dados_de_remuneracao import ValidadorDadosDeRemuneracao

def pipeline_servidores(keywords, job_name):

    # Subtag - Dados dos Servidores
    # validador_dados_dos_servidores = ValidadorDadosDosServidores(job_name, keywords['dados_dos_servidores'])
    # output_dados_dos_servidores = validador_dados_dos_servidores.predict()
    # print(output_dados_dos_servidores)

    # Registro da remuneração
    # validador_registro_da_remuneracao = ValidadorRegistroDaRemuneracao(job_name, keywords['registro_da_remuneracao'])
    # output_registro_da_remuneracao = validador_registro_da_remuneracao.predict()
    # print(output_registro_da_remuneracao)
    
    # Registro por lotação
    # validador_registro_por_lotacao = ValidadorRegistroPorLotacao(job_name, keywords['registro_por_lotacao'])
    # output_registro_por_lotacao = validador_registro_por_lotacao.predict()
    # print("output_registro_por_lotacao:")
    # print(output_registro_por_lotacao)

    # Auxilios
    # "Fazer com o template Betha"
    # validador_auxilios = ValidadorAuxilios(job_name, keywords['auxilios'])
    # output_auxilios = validador_auxilios.predict()
    # print("output_auxilios:")
    # print(output_auxilios)

    # Proventos de aposentadoria
    # validador_proventos_de_aposentadoria = ValidadorProventosDeAposentadoria(job_name, keywords['proventos_de_aposentadoria'])
    # output_proventos_de_aposentadoria = validador_proventos_de_aposentadoria.predict()
    # print("output_proventos_de_aposentadoria:")
    # print(output_proventos_de_aposentadoria)

    # Proventos de pensão
    validador_proventos_de_pensao = ValidadorProventosDePensao(job_name, keywords['proventos_de_pensao'])
    output_proventos_de_pensao = validador_proventos_de_pensao.predict()
    print("output_proventos_de_pensao:")
    print(output_proventos_de_pensao)
    
    # Relatório mensal
    # validador_relatorio_mensal = ValidadorRelatorioMensal(job_name, keywords['relatorio_mensal'])
    # output_relatorio_mensal = validador_relatorio_mensal.predict()
    # print("output_relatorio_mensal:")
    # print(output_relatorio_mensal)
    
    # Dados de remuneração
    # validador_dados_de_remuneracao = ValidadorDadosDeRemuneracao(job_name, keywords['dados_de_remuneracao'])
    # output_dados_de_remuneracao = validador_dados_de_remuneracao.predict()
    # print("output_dados_de_remuneracao:")
    # print(output_dados_de_remuneracao)


    result = handle_files.abrir_existente(job_name)

    # result['78'] = output_dados_dos_servidores['nome']['predict']
    # result['79'] = output_dados_dos_servidores['cargo_funcao']['predict']
    # result['80'] = output_dados_dos_servidores['remuneracao']['predict']
    # result['81'] = output_registro_da_remuneracao['agentes_politicos']['predict']
    # result['82'] = output_registro_da_remuneracao['contratados_temporariamente']['predict']
    # result['83'] = output_registro_da_remuneracao['servidores_efetivos_ou_empregados_publicos']['predict']
    # result['84'] = output_registro_por_lotacao['matricula']['predict']
    # result['85'] = output_registro_por_lotacao['nome']['predict']
    # result['86'] = output_registro_por_lotacao['cargo_funcao']['predict']
    # result['87'] = output_registro_por_lotacao['remuneracao']['predict']
    # result['88'] = output_registro_por_lotacao['abate_teto']['predict']
    # result['89'] = output_registro_por_lotacao['tipo_de_vinculo']['predict']
#     result['90'] = output_auxilios['verbas_indenizatorias']['predict']
#     result['91'] = output_auxilios['ajudas_de_custos']['predict']
#     result['92'] = output_auxilios['jetons']['predict']
#     result['93'] = output_auxilios['vantagens_pecuniarias']['predict']
#     # 94 - Exigência direcionada a câmera 
    # result['95'] = output_proventos_de_aposentadoria['nome']['predict']
    # result['96'] = output_proventos_de_aposentadoria['cargo']['predict']
    # result['97'] = output_proventos_de_aposentadoria['remuneracao']['predict']
    # result['98'] = output_proventos_de_aposentadoria['abate_teto']['predict']
    # result['99'] = output_proventos_de_aposentadoria['remuneracao_retirando_o_abate_teto']['predict']
    # result['100'] = output_proventos_de_aposentadoria['tipo_de_vinculo']['predict']
    result['101'] = output_proventos_de_pensao['nome']['predict']
    result['102'] = output_proventos_de_pensao['cargo']['predict']
    result['103'] = output_proventos_de_pensao['remuneracao']['predict']
    result['104'] = output_proventos_de_pensao['abate_teto']['predict']
    result['105'] = output_proventos_de_pensao['abate_teto']['predict']
    result['106'] = output_proventos_de_pensao['tipo_de_vinculo']['predict']


#     result['107'] = output_relatorio_mensal['despesa_com_pessoal']['predict']

#     # Dados de remuneração
#     validador_dados_de_remuneracao = ValidadorDadosDeRemuneracao(job_name, keywords[''])
#     output_dados_de_remuneracao = validador_dados_de_remuneracao.predict()
#     result['108'] = output_dados_de_remuneracao['objeto']['predict']
#     result['109'] = output_dados_de_remuneracao['conveniados']['predict']
#     result['110'] = output_dados_de_remuneracao['aditivos']['predict']

    handle_files.save_dict_in_json(job_name, result)
