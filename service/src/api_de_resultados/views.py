from flask import jsonify
from flask import Blueprint
from src.api_de_integracao.manage_resultado import procurar_resultado, Resposta
from src.municipio.manage_municipios import is_valid_ibge_code, obter_codigo_ibge_pelo_nome

api_de_resultados = Blueprint(
    'api_de_resultados', __name__)


@api_de_resultados.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":

        try:
            municipio_id = int(municipio)
        except ValueError:
            municipio_id = obter_codigo_ibge_pelo_nome(municipio)

        if municipio_id is None or not is_valid_ibge_code(municipio_id):
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

        resultado = procurar_resultado(municipio_id)
        return jsonify(resultado)


@api_de_resultados.route('/<municipio>/<item_id>', methods=['GET'])
def getItem(municipio, item_id):

    try:
        municipio_id = int(municipio)
    except ValueError:
        municipio_id = obter_codigo_ibge_pelo_nome(municipio)

    if municipio_id is None:
        return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

    resultado = procurar_resultado(municipio_id, item_id)
    if resultado is None:
        return jsonify(Resposta.ITEM_NAO_DISPONIVEL.to_dict())
    else:
        return jsonify(resultado)
