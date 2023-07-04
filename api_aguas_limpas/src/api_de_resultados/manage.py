from src.api_de_resultados.models import Municipio

def is_valid_ibge_code(cod_ibge):
    id_ibge = Municipio.query.filter_by(
        id_ibge=cod_ibge).first()
    if id_ibge:
        return True
    else:
        return False

def get_municipio_pelo_codigo_ibge(cod_ibge):
    municipio = Municipio.query.filter_by(
        id_ibge=cod_ibge).first()
    return municipio

def obter_codigo_ibge_pelo_nome(nome_do_municipio):
    codigo_ibge = None
    municipio = Municipio.query.filter_by(
        nome_formatado=nome_do_municipio).first()
    if municipio is not None:
        codigo_ibge = municipio.id_ibge
    return codigo_ibge
