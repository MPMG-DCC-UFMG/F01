from enum import Enum
from flask import jsonify
from flask import Blueprint, render_template
from src.api_de_integracao.manage_resultado import procurar_resultado
from src.api_de_integracao.manage_cod_resposta import Resposta
from src.municipio.manage_municipios import obter_codigo_ibge_pelo_nome

api_de_resultados = Blueprint(
    'api_de_resultados', __name__)



@api_de_resultados.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":

        try:
            municipio_id = int(municipio)
        except ValueError:
            municipio_id = obter_codigo_ibge_pelo_nome(municipio)

        if municipio_id is None:
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

        resultado = procurar_resultado(municipio_id)
        if resultado is None:
            return jsonify(Resposta.ITEM_NAO_DISPONIVEL.to_dict())
        else:
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
