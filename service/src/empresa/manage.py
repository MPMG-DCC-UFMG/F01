from src.empresa.models import Empresa

def get_template(nome_do_template):

    nome_no_git_hub = {
        'habeas_data': "habeas_data_(7)",
        'betha': "betha_(26)",
        'pt': "pt_(45)",
        'adpm': "adpm_(22)",
        'abo': "abo_(21)",
        'fiorilli': "fiorilli_sociedade_civil_(7)",
        'memory': "memory_(6)",
        'grp': "grp_(27)",
        'template2': "template2_(28)",
        'template1_(22)': "template1_(22)",
        'siplanweb': "siplanweb_(61)",
        'sintese_tecnologia_informatica': "sintese_tecnologia_e_informatica_(88)",
        'portal_facil_(5)': "portal_facil_(5)",
    }

    if (nome_do_template in nome_no_git_hub):
        nome_do_template = nome_no_git_hub[nome_do_template]

    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template

def get_municipios_do_template(nome_do_template):
    template = Empresa.query.filter_by(nome=nome_do_template).first()
    return template.municipios

