import os
from flask import Flask, render_template, redirect, flash, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "jvkbsiuehrq7h"

############################################################
################## BANCO DE DADOS ##########################
############################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#############################################################
#######################  BLUEPRINTS ##########################
#############################################################

from sistema.principal.views import principal
from sistema.municipio.views import municipio
from sistema.empresa.views import empresa
from sistema.api_de_resultados.views import api
from sistema.coletor.views import coletor
from sistema.validador.views import validador

app.register_blueprint(principal)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(municipio, url_prefix="/municipio")
app.register_blueprint(empresa, url_prefix="/empresa")
app.register_blueprint(coletor, url_prefix="/coletor")
app.register_blueprint(validador, url_prefix="/validador")
