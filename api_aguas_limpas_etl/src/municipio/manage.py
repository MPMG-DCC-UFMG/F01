import os
from src import db
import pandas as pd
from src.municipio.models import Municipio
from src.api_de_integracao.manage import formatar_nome


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
    print("municipio", municipio)
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


def get_codigo_ibge_pelo_id(id):
    municipio = Municipio.query.filter_by(
        id=id).first()
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


def carregar_municipios():
    if len(Municipio.query.all()):
        return
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/links_validados.csv')

    Municipio.query.delete()

    # Coloca o id_ibge com base na lista_municipios.csv
    codigos_ibge = []
    df_municipios = pd.read_csv(dir_path + '/lista_municipios.csv', index_col='nome')

    for _, row in df.iterrows():
        nome_do_municipio = row['Município']
        municipio_com_codigo = df_municipios.loc[nome_do_municipio]
        codigo_ibge_do_municipio = municipio_com_codigo['id']
        codigos_ibge.append(municipio_com_codigo['id']) 

        nome_formatado = formatar_nome(row['Município']) 

        municipio = inserir_municipios(nome=row['Município'],
                                            nome_formatado=nome_formatado,
                                            url_site_prefeitura=row['Site Prefeitura'],
                                            url_portal=row['Portal da Transparência (validado)'],
                                            id_ibge=int(codigo_ibge_do_municipio))

    df['id_ibge'] = codigos_ibge
    df.to_csv(dir_path + '/links_validados.csv', index=False)
