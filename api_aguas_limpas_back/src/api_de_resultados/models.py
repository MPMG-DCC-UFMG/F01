from src import db
from datetime import datetime, timedelta

MunicipioxEmpresa = db.Table(
    'municipioxempresa',
    db.Column('id_municipio', db.Integer, db.ForeignKey('municipio.id'), primary_key=True),
    db.Column('id_empresa', db.Integer, db.ForeignKey('empresa.id')), primary_key=True)


class Empresa(db.Model):
    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)

    municipios = db.relationship("Municipio",
                                 secondary=MunicipioxEmpresa,
                                 back_populates="empresa")

class Municipio(db.Model):
    __tablename__ = "municipio"

    id = db.Column(db.Integer, primary_key=True)
    id_ibge = db.Column(db.Integer, nullable=True)
    nome = db.Column(db.String(30), nullable=False)
    nome_formatado = db.Column(db.String(30), nullable=True)
    url_site_prefeitura = db.Column(db.String(100), nullable=True)
    url_portal = db.Column(db.String(1000), nullable=True)

    empresa = db.relationship("Empresa",
                                 secondary=MunicipioxEmpresa,
                                 back_populates="municipios")

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    subtags = db.relationship('Subtag', backref = 'tag')
    itens = db.relationship('Item', backref = 'tag')

class Subtag(db.Model):
    __tablename__ = "subtag"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    itens = db.relationship('Item', backref = 'item')

class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    abreviacao = db.Column(db.String(50), nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    subtag_id = db.Column(db.Integer, db.ForeignKey('subtag.id'))

class Resultado(db.Model):
    __tablename__ = "resultado"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, db.ForeignKey('tag.id'))
    subtag_id = db.Column(db.Integer, db.ForeignKey('subtag.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id'))
    municipio_id_ibge = db.Column(db.Integer, nullable=True)

    codigo_resposta = db.Column(db.String(30), nullable=True)
    #exemplo: OK, BLOQUEADA, NAO_COLETAVEL_TIMEOUT, TRUE, FALSE

    justificativa = db.Column(db.String(1000), nullable=True)
    # "Item ainda não validado"
    # "Validacao informou que o item coletado nao atende aos requisitos"

    #Salvando a data e hora atuais 
    data_validacao = db.Column(db.DateTime, default=(datetime.utcnow() - timedelta(hours=3)), nullable=True)