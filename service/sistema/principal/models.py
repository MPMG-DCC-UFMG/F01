from sistema import app, db

class Resultado(db.Model):
    __tablename__ = "resultado"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=True)

