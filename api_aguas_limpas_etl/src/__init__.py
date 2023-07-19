from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "jvkbsiuehrq7h"
app.config['JSON_AS_ASCII'] = False

################### BANCO DE DADOS ##########################

app.config.from_object("src.config.Config")
db = SQLAlchemy(app)


#######################  BLUEPRINTS ##########################

from src.api_de_integracao.views import api_de_integracao
from src.validadores.views import validadores
from src.municipio.views import municipio
from src.empresa.views import empresa
from src.checklist.views import checklist


from src.municipio.manage import carregar_municipios
from src.empresa.manage import carregar_templates
from src.checklist.manage import carregar_checklist
from src.api_de_integracao.views import subir_resultados

app.register_blueprint(api_de_integracao)
app.register_blueprint(validadores, url_prefix="/validadores")
app.register_blueprint(municipio, url_prefix="/municipio")
app.register_blueprint(empresa, url_prefix="/empresa")
app.register_blueprint(checklist, url_prefix="/checklist")

with app.app_context():
    try:
        db.create_all()
    except:
        print("Erro ao criar o banco")
    carregar_municipios()
    carregar_templates()
    carregar_checklist()
    subir_resultados()
    print("Resultados ok")
    db.session.commit()