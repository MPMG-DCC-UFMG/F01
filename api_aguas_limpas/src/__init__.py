from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "jvkb3333rwsiuehrq7h"
app.config['JSON_AS_ASCII'] = False
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)

#######################  BLUEPRINTS ##########################

from src.api_de_resultados.views import api_de_resultados

app.register_blueprint(api_de_resultados, url_prefix="/api")
