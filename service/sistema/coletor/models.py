from sistema import db


class Coletor(db.Model):
    __tablename__ = "coletor"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
