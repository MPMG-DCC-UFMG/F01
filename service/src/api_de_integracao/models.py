from src import db
from src.checklist.models import Tag, Subtag, Item

class Resultado(db.Model):
    __tablename__ = "resultado"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, db.ForeignKey('tag.id'))
    subtag_id = db.Column(db.Integer, db.ForeignKey('subtag.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id_ibge'))
    codigo_resposta = db.Column(db.String(30), nullable=True)
    descricao = db.Column(db.String(100), nullable=True)
    justificativa = db.Column(db.String(300), nullable=True)