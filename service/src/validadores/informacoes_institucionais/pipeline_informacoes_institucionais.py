from src.validadores.utils import handle_files
from src.validadores.informacoes_institucionais.estrutura_organizacional import ValidadorEstruturaOrganizacional
from src.validadores.informacoes_institucionais.unidades_administrativas import ValidadorUnidadesAdministrativas
from src.validadores.informacoes_institucionais.link_de_acesso import ValidadorLinkDeAcesso


def pipeline_informacoes_institucionais(keywords, job_name):
    try:
        keywords = keywords['informacoes_institucionais']
    except KeyError:
        return None

    informacoes_institucionais = {
        'estrutura_organizacional': {},
    }


    # Subtag - Estrutura organizacional
    validador_estrutura_organizacional = ValidadorEstruturaOrganizacional(job_name, keywords['estrutura_organizacional'])
    informacoes_institucionais['estrutura_organizacional'] = validador_estrutura_organizacional.predict()

    # # Subtag - Unidades administrativas
    # validador_unidades_administrativas = ValidadorUnidadesAdministrativas(job_name, keywords['unidades_administrativas'])
    # informacoes_institucionais['unidades_administrativas'] = validador_unidades_administrativas.predict()

    print('Result pipeline:', informacoes_institucionais)

    # Subtag - Registro das competências TODO


    # Subtag - Link de Acesso
    # validador_link_de_acesso = ValidadorLinkDeAcesso(job_name, keywords['link_de_acesso'])
    # informacoes_institucionais['link_de_acesso'] = validador_link_de_acesso.predict()

    # Subtag - Conselhos Municipais TODO

