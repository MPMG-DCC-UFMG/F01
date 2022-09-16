from src import db
from src.municipio.models import MunicipioxEmpresa


class Empresa(db.Model):
    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)

    municipios = db.relationship("Municipio",
                                 secondary=MunicipioxEmpresa,
                                 back_populates="empresa")
