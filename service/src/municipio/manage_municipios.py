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


def obter_url_portal(nome_do_municipio):

    url_portal = Municipio.query.filter_by(
        nome_formatado=nome_do_municipio).first().url_portal
    return url_portal


def obter_codigo_ibge_pelo_nome(nome_do_municipio):
    codigo_ibge = None
    municipio = Municipio.query.filter_by(
        nome_formatado=nome_do_municipio).first()
    if municipio is not None:
        codigo_ibge = municipio.id_ibge
    return codigo_ibge


def get_municipio(nome_do_municipio):
    municipio = Municipio.query.filter_by(
        nome_formatado=nome_do_municipio).first()
    return municipio

def get_municipio_pelo_codigo_ibge(cod_ibge):
    municipio = Municipio.query.filter_by(
        id_ibge=cod_ibge).first()
    return municipio


def is_valid_ibge_code(cod_ibge):
    id_ibge = Municipio.query.filter_by(
        id_ibge=cod_ibge).first()
    if id_ibge:
        return True
    else:
        return False

def get_all_municipios():
    municipios = Municipio.query.all()
    return municipios