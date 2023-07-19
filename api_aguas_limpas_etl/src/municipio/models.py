from src import app, db

MunicipioxEmpresa = db.Table(
    'municipioxempresa',
    db.Column('id_municipio', db.Integer, db.ForeignKey('municipio.id'), primary_key=True),
    db.Column('id_empresa', db.Integer, db.ForeignKey('empresa.id')), primary_key=True)


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

