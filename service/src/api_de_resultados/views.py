from enum import Enum
from flask import jsonify
from flask import Blueprint, render_template
from src.api_de_integracao.manage import procurar_resultado
from src.municipio.manage_municipios import obter_codigo_ibge_pelo_nome

api_de_resultados = Blueprint(
    'api_de_resultados', __name__)


class Resposta(Enum):
    OK = 0  # Item validado com sucesso
    ITEM_NAO_DISPONIVEL = 1  # Erro generico para item
    MUNICIPIO_NAO_DISPONIVEL = 2  # Erro generico para municipio
    NAO_COLETADO = 3  # Item nao encontrado no portal de transparencia
    NAO_COLETADO_ERRO_TIMEOUT = 4  # Item encontrado, mas houve erro de timeout na coleta
    NAO_VALIDADO = 5  # Validacao informou que o item coletado nao atende aos requisitos

    def to_dict(self):
        return {'resposta': self.value, 'justificativa': self.name}


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
