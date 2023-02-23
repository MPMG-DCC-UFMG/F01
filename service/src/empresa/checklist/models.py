from src import app, db

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