from src.empresa.models import Empresa
from src.api_de_integracao.manage import formatar_nome

def get_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template

def get_municipios_do_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template.municipios

def get_nome_dos_municipios_do_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    municipios = [formatar_nome(municipio.nome) for municipio in template.municipios]
    return municipios

