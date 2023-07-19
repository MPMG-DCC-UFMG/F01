from src import db
from datetime import datetime, timedelta
from src.checklist.models import Tag, Subtag, Item

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