from src.validadores.utils import handle_files
from src.validadores.servidores_publicos.dados_dos_servidores import ValidadorDadosDosServidores
from src.validadores.servidores_publicos.registro_da_remuneracao import ValidadorRegistroDaRemuneracao
from src.validadores.servidores_publicos.registro_por_lotacao import ValidadorRegistroPorLotacao
from src.validadores.servidores_publicos.auxilios import ValidadorAuxilios
from src.validadores.servidores_publicos.proventos_de_aposentadoria import ValidadorProventosDeAposentadoria
from src.validadores.servidores_publicos.proventos_de_pensao import ValidadorProventosDePensao
from src.validadores.servidores_publicos.relatorio_mensal import ValidadorRelatorioMensal
from src.validadores.servidores_publicos.dados_de_remuneracao import ValidadorDadosDeRemuneracao

def pipeline_servidores_publicos(keywords, job_name):

    try:
        keywords = keywords['servidores_publicos']
    except KeyError:
        return None

    servidores_publicos = {
        'dados_dos_servidores': {},
    }

    # Subtag - Dados dos Servidores
    # validador_dados_dos_servidores = ValidadorDadosDosServidores(job_name, keywords['dados_dos_servidores'])
    # servidores_publicos['dados_dos_servidores'] = validador_dados_dos_servidores.predict()

    # Registro da remuneração
    # validador_registro_da_remuneracao = ValidadorRegistroDaRemuneracao(job_name, keywords['registro_da_remuneracao'])
    # servidores_publicos['registro_da_remuneracao'] = validador_registro_da_remuneracao.predict()
    
    # Registro por lotação
    # validador_registro_por_lotacao = ValidadorRegistroPorLotacao(job_name, keywords['registro_por_lotacao'])
    # servidores_publicos['registro_por_lotacao'] = validador_registro_por_lotacao.predict()
    # print("output_registro_por_lotacao:")
    # print(output_registro_por_lotacao)


    # Auxilios
    # validador_auxilios = ValidadorAuxilios(job_name, keywords['auxilios'])
    # servidores_publicos['auxilios'] = validador_auxilios.predict()

    # Rodar

    # Proventos de aposentadoria
    # validador_proventos_de_aposentadoria = ValidadorProventosDeAposentadoria(job_name, keywords['proventos_de_aposentadoria'])
    # servidores_publicos['proventos_de_aposentadoria'] = validador_proventos_de_aposentadoria.predict()

    # Proventos de pensão
    # validador_proventos_de_pensao = ValidadorProventosDePensao(job_name, keywords['proventos_de_pensao'])
    # servidores_publicos['proventos_de_pensao'] = validador_proventos_de_pensao.predict()
    
    # Relatório mensal
    # validador_relatorio_mensal = ValidadorRelatorioMensal(job_name, keywords['relatorio_mensal'])
    # servidores_publicos['relatorios_despesas_com_pessoal'] = validador_relatorio_mensal.predict()
    
    # Dados de remuneração
    validador_dados_de_remuneracao = ValidadorDadosDeRemuneracao(job_name, keywords['dados_de_remuneracao'])
    servidores_publicos["dados_de_remuneracao"] = validador_dados_de_remuneracao.predict()


    return servidores_publicos