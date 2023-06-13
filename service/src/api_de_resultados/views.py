from flask import jsonify
from flask import Blueprint
from src.api_de_integracao.manage import procurar_resultado, Resposta
from src.municipio.manage_municipios import get_municipio_pelo_codigo_ibge, is_valid_ibge_code, obter_codigo_ibge_pelo_nome

api_de_resultados = Blueprint(
    'api_de_resultados', __name__)


@api_de_resultados.route('/', methods=['GET'])
def index():
    return jsonify('Api de resultados ok')


@api_de_resultados.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":

        try:
            codigo_ibge = int(municipio)
        except ValueError:
            codigo_ibge = obter_codigo_ibge_pelo_nome(municipio)

        if codigo_ibge is None or not is_valid_ibge_code(codigo_ibge):
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

        municipio = get_municipio_pelo_codigo_ibge(codigo_ibge)
        if municipio is None:
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())
        resultado = procurar_resultado(municipio.id)
        if not len(resultado):
            return jsonify(Resposta.MUNICIPIO_NAO_VALIDADO.to_dict())

        return jsonify(resultado)


@api_de_resultados.route('/<municipio>/<item_id>', methods=['GET'])
def getItem(municipio, item_id):

    # Pelo nome do município
    try:
        codigo_ibge = int(municipio)
    except ValueError:
        codigo_ibge = obter_codigo_ibge_pelo_nome(municipio)

    # Pelo código do município
    print(codigo_ibge)
    if codigo_ibge is None:
        return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

    municipio = get_municipio_pelo_codigo_ibge(codigo_ibge)
    if municipio is None:
        return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())
    resultado = procurar_resultado(municipio.id, item_id)

    if resultado is None:
        return jsonify(Resposta.ITEM_NAO_DISPONIVEL.to_dict())
    else:
        return jsonify(resultado)