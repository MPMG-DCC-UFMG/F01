from src.validadores.informacoes_institucionais.estrutura_organizacional import ValidadorEstruturaOrganizacional
from src.validadores.informacoes_institucionais.unidades_administrativas import ValidadorUnidadesAdministrativas
from src.validadores.informacoes_institucionais.leis_municipais import ValidadorLeisMunicipais
from src.validadores.informacoes_institucionais.registro_das_competencias import ValidadorRegistroDasCompetencias
from src.validadores.informacoes_institucionais.conselhos_municipais import ValidadorConselhosMunicipais

def pipeline_informacoes_institucionais(keywords, job_name):
    try:
        keywords = keywords['informacoes_institucionais']
    except KeyError:
        return None

    informacoes_institucionais = {}

    # Subtag - Estrutura organizacional
    try:
        keywords_validador = keywords['estrutura_organizacional']
    except KeyError:
        pass
    else:
        validador_estrutura_organizacional = ValidadorEstruturaOrganizacional(job_name, keywords_validador)
        informacoes_institucionais['estrutura_organizacional'] = validador_estrutura_organizacional.predict()

    # Subtag - Unidades administrativas
    try:
        keywords_validador = keywords['unidades_administrativas']
    except KeyError:
        pass
    else:
        validador_unidades_administrativas = ValidadorUnidadesAdministrativas(job_name, keywords_validador)
        informacoes_institucionais['unidades_administrativas'] = validador_unidades_administrativas.predict()

    # Subtag - Registro das competências
    try:
        keywords_validador = keywords['registro_das_competencias']
    except KeyError:
        pass
    else:
        validador_registro_das_competencias = ValidadorRegistroDasCompetencias(job_name, keywords_validador)
        informacoes_institucionais['registro_das_competencias'] = validador_registro_das_competencias.predict()

    # Subtag - Leis Municipais
    try:
        keywords_validador = keywords['leis_municipais']
    except KeyError:
        pass
    else:
        validador_leis_municipais = ValidadorLeisMunicipais(job_name, keywords_validador)
        informacoes_institucionais['leis_municipais'] = validador_leis_municipais.predict()

    # Subtag - Conselhos Municipais
    try:
        keywords_validador = keywords['conselhos_municipais']
    except KeyError:
        pass
    else:
        validador_conselhos_municipais = ValidadorConselhosMunicipais(job_name, keywords['conselhos_municipais'])
        informacoes_institucionais['conselhos_municipais'] = validador_conselhos_municipais.predict()
    
    return informacoes_institucionais