from flask import jsonify
from flask import Blueprint
from src.api_de_integracao.manage import procurar_resultado, Resposta
from src.municipio.manage_municipios import get_municipio_pelo_codigo_ibge, is_valid_ibge_code, obter_codigo_ibge_pelo_nome, get_all_municipios
from src.checklist.manage import get_all_itens
import pandas as pd


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
<<<<<<< HEAD
        return jsonify(resultado)
=======
        return jsonify(resultado)
    

@api_de_resultados.route('/gerar_csv', methods=['GET'])

# novo_resultado = Resultado(item_id=item_id,
#                                    municipio_id=municipio_id,
#                                    codigo_resposta=codigo_resposta,
#                                    data_validacao = datetime.utcnow() - timedelta(hours=3),
#                                    justificativa=justificativa)

def gerar_csv():
    municipios = get_all_municipios()

    df = pd.DataFrame(columns=['id_municipio', 'id_item', 'codigo_resposta', 'validated_at', 'justificativa'])

    # Loop pelos municípios
    for municipio in municipios:

        itens = get_all_itens()
        for item in itens:
            resultado = procurar_resultado(municipio.id, item.id)

            # Criar um dicionário com os valores
            data = {
                'id_municipio': municipio.id,
                'id_item': item.id,
            }

            if resultado:

                try:
                    data['codigo_resposta'] = resultado[item.id]['codigo_resposta']
                except AttributeError:
                    pass
                try:
                    data['validated_at'] = resultado[item.id]['validated_at']
                except AttributeError:
                    pass
                try:
                    data['justificativa'] = resultado[item.id]['justificativa']
                except AttributeError:
                    pass

                 # Adicionar uma linha ao DataFrame
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Exibir o DataFrame final
    df.to_csv("resultados.csv")
    return jsonify("ok")
>>>>>>> 2aa6fdb3568ada6779394a4e68092f9a5a0f098b
