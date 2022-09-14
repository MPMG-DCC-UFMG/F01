from src import db
from src.municipio.models import Municipio


def inserir_municipios(nome, nome_formatado, url_site_prefeitura, url_portal, id_ibge):
    novo_municipio = Municipio(nome=nome,
                               nome_formatado=nome_formatado,
                               url_site_prefeitura=url_site_prefeitura,
                               url_portal=url_portal,
                               id_ibge=id_ibge)

    db.session.add(novo_municipio)
    db.session.commit()

    return novo_municipio


def obter_codigo_ibge_pelo_nome(nome_do_municipio):

    id_ibge = Municipio.query.filter_by(
        nome_formatado=nome_do_municipio).first().id_ibge
    return id_ibge
