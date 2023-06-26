import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "jvkbsiuehrq7h"
app.config['JSON_AS_ASCII'] = False

# ################## BANCO DE DADOS ##########################

# basedir = os.path.abspath(os.path.dirname(__file__))
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
# #     os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://asafe:123@localhost:5432/flask_db_f01'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# Migrate(app, db)


app.config.from_object("src.config.Config")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

#######################  BLUEPRINTS ##########################

from src.api_de_integracao.views import api_de_integracao
from src.validadores.views import validadores
from src.municipio.views import municipio
from src.empresa.views import empresa
from src.api_de_resultados.views import api_de_resultados
from src.checklist.views import checklist

app.register_blueprint(api_de_integracao)
app.register_blueprint(validadores, url_prefix="/validadores")
app.register_blueprint(api_de_resultados, url_prefix="/api")
app.register_blueprint(municipio, url_prefix="/municipio")
app.register_blueprint(empresa, url_prefix="/empresa")
app.register_blueprint(checklist, url_prefix="/checklist")
