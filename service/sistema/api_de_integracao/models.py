from sistema import db


class Resultado(db.Model):
    __tablename__ = "resultado"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, db.ForeignKey('tag.id'))
    subtag_id = db.Column(db.Integer, db.ForeignKey('subtag.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id_ibge'))
    resposta = db.Column(db.String(100), nullable=True)
