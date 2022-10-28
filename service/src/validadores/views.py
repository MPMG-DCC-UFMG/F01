from flask import jsonify
from flask import Blueprint

from src.municipio.manage_municipios import get_municipio
from src.api_de_integracao.manage import salvar_resultado_de_json
from src.empresa.manage import get_nome_dos_municipios_do_template
from src.validadores.utils.handle_files import get_keywords_do_template

validadores = Blueprint('validadores', __name__)

from src.validadores import pipeline_validadores

@validadores.route('/')
def index():
    print('validadores')
    return jsonify('Validadores.')


# templates = ['abo_21', 'sintese', 'betha', 'siplanweb', 'pt_45', 'memory_66']

@validadores.route('/<string:nome_do_template>', methods=['POST', 'GET'])
def rodar_template(nome_do_template):

    parametros = get_keywords_do_template(nome_do_template)
    municipios = get_nome_dos_municipios_do_template(nome_do_template)

    for municipio in municipios:

        # if municipio == "salinas": #em testes
            print(municipio)
            resultado = pipeline_validadores.todas_tags(parametros, municipio)

            municipio = get_municipio(municipio)
            print("resultado final")
            print(resultado)
            print("Salvando resultado")

            salvar_resultado_de_json(municipio_id=municipio.id, resultado_json=resultado)

    return jsonify(f"Template {nome_do_template} validado") 
