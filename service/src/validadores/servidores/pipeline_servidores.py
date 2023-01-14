from src.validadores.utils import handle_files
from src.validadores.servidores.dados_dos_servidores import ValidadorDadosDosServidores
from src.validadores.servidores.registro_da_remuneracao import ValidadorRegistroDaRemuneracao
from src.validadores.servidores.registro_por_lotacao import ValidadorRegistroPorLotacao
from src.validadores.servidores.auxilios import ValidadorAuxilios
from src.validadores.servidores.proventos_de_aposentadoria import ValidadorProventosDeAposentadoria
from src.validadores.servidores.proventos_de_pensao import ValidadorProventosDePensao
from src.validadores.servidores.relatorio_mensal import ValidadorRelatorioMensal
from src.validadores.servidores.dados_de_remuneracao import ValidadorDadosDeRemuneracao

def pipeline_servidores(keywords, job_name):

    try:
        keywords = keywords['servidores']
    except KeyError:
        return None

    servidores = {
        'empenhos': {},
        'pagamentos': {},
        'consulta_favorecido': {},
        'gerar_relatorios': {},
        'relatorios': {}
    }
    

    # Subtag - Dados dos Servidores
    validador_dados_dos_servidores = ValidadorDadosDosServidores(job_name, keywords['dados_dos_servidores'])
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
    # validador_proventos_de_pensao = ValidadorProventosDePensao(job_name, keywords['proventos_de_pensao'])
    # output_proventos_de_pensao = validador_proventos_de_pensao.predict()
    # print("output_proventos_de_pensao:")
    # print(output_proventos_de_pensao)
    
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

     # Dados de remuneração
#     validador_dados_de_remuneracao = ValidadorDadosDeRemuneracao(job_name, keywords[''])
#     output_dados_de_remuneracao = validador_dados_de_remuneracao.predict()
