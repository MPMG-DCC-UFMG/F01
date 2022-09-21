from src.api_de_integracao.manage_resultado import formatar_nome
from src import db
from flask import jsonify
from flask import Blueprint

from src.empresa.manage import get_nome_dos_municipios_do_template
from src.validadores.utils.handle_files import get_keywords_do_template

validadores = Blueprint('validadores', __name__)

from src.validadores import pipeline_validadores

@validadores.route('/')
def index():
    print('validadores')
    return jsonify('Validadores.')


# templates = ['abo_(21)', 'sintese', 'betha', 'siplanweb']

@validadores.route('/<string:nome_do_template>', methods=['POST', 'GET'])
def rodar_template(nome_do_template):

    parametros = get_keywords_do_template(nome_do_template)
    municipios = get_nome_dos_municipios_do_template(nome_do_template)

    for municipio in municipios:

        if municipio == "muriae": #em testes
            print(municipio)
            resultado = pipeline_validadores.todas_tags(parametros, municipio)
            print(resultado)

    return jsonify(f"Template {nome_do_template} validado") 
