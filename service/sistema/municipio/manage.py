from sistema import db
from sistema.municipio.models import Municipio

def insert_municipio(nome, url_site_prefeitura, url_portal):
    novo_municipio = Municipio(nome=nome,
                              url_site_prefeitura=url_site_prefeitura,
                              url_portal=url_portal)

    db.session.add(Municipio)
    db.session.commit()
    
    return novo_municipio