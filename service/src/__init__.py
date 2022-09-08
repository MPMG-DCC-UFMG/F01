import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "jvkbsiuehrq7h"

################## BANCO DE DADOS ##########################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#######################  BLUEPRINTS ##########################

from src.api_de_integracao.views import api_de_integracao
from src.municipio.views import municipio
from src.empresa.views import empresa
from src.api_de_resultados.views import api_de_resultados
from src.coletor.views import coletor

app.register_blueprint(api_de_integracao)
app.register_blueprint(api_de_resultados, url_prefix="/api")
app.register_blueprint(municipio, url_prefix="/municipio")
app.register_blueprint(empresa, url_prefix="/empresa")
app.register_blueprint(coletor, url_prefix="/coletor")
