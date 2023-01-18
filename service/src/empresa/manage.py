from src.empresa.models import Empresa
from src.api_de_integracao.manage import formatar_nome

def get_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template

def get_nome_dos_templates():
    templates = Empresa.query.all()
    if len(templates):
        templates = [template.nome for template in templates]
    return templates

def get_municipios_do_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template.municipios

def get_nome_dos_municipios_do_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    municipios = [formatar_nome(municipio.nome) for municipio in template.municipios]
    return municipios


def get_nome_dos_municipios_do_template_sem_formatar(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    municipios = [municipio.nome for municipio in template.municipios]
    return municipios

