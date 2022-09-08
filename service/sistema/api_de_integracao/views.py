import json
from sistema import db
from flask import jsonify
from sistema.empresa.models import Empresa
from flask import Blueprint, render_template
from sistema.municipio.models import Municipio
from sistema.api_de_integracao.manage import salvar_resultado
from sistema.municipio.manage_municipios import formatar_nome_de_municipio, obter_codigo_ibge_pelo_nome

api_de_integracao = Blueprint('api_de_integracao', __name__)


@api_de_integracao.route('/')
def index():
    municipios = Municipio.query.all()
    empresas = Empresa.query.all()

    return jsonify('ok')


@api_de_integracao.route('/carregar_resultados', methods=['GET'])
def carregarResultados():

    municipios = Municipio.query.all()
    count = 0
    for municipio in municipios:

        nome_formatado = formatar_nome_de_municipio(municipio.nome)
        codigo_ibge = obter_codigo_ibge_pelo_nome(nome_formatado)

        try:
            with open('../results/' + nome_formatado + '.json', 'r') as myfile:
                data = myfile.read()
                resultados_do_municipio = json.loads(data)
                for item_id in resultados_do_municipio:
                    count += 1
                    salvar_resultado(
                        resultado=resultados_do_municipio[item_id], municipio_id=codigo_ibge, item_id=item_id)

        except FileNotFoundError:
            pass

    return jsonify([count])
