from flask import jsonify
from flask import Blueprint
from src.api_de_integracao.manage import procurar_resultado, Resposta
from src.municipio.manage_municipios import get_municipio_pelo_codigo_ibge, is_valid_ibge_code, obter_codigo_ibge_pelo_nome, get_all_municipios
from src.checklist.manage import get_all_itens
import pandas as pd


api_de_resultados = Blueprint(
    'api_de_resultados', __name__)


@api_de_resultados.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):
    """Consulta de todos os itens de um municipio.
    Este endpoint permite consulta o resultado da validação de um município com base no seu código IBGE.

    1. Se o código IBGE for inválido ou não for encontrado, retorna uma resposta JSON informando que o município não está disponível.
    2. Caso contrário, obtém o objeto do município correspondente ao código IBGE.
    3. Realiza uma busca por um resultado relacionado ao município.
    4. Retorna uma resposta JSON contendo o resultado encontrado.
    
    O código lida com a entrada do usuário, verifica se é um código IBGE válido ou um nome de município. Em seguida, busca o resultado correspondente ao município e retorna como resposta JSON.
    
    ---
    tags:
      - Resultados
    parameters:
      - name: municipio
        in: path
        type: string
        required: true
        description: ID do municipio (código IBGE).
    definitions:
      <numero_do_item>:
        type: object
        properties:
          codigo_resposta:
            type: string
          validated_at:
            type: string
            format: date-time
          justificativa:
            type: string

      OuterObject:
        type: object
        properties:
          <numero_do_item>:
            $ref: '#/definitions/<numero_do_item>'

      ListOfOuterObjects:
        type: array
        items:
          $ref: '#/definitions/OuterObject'

    responses:
      200:
        description: Lista no formato `JSON` em que cada item contém um objeto com a resposta para o item. A lista tem a resposta de todos os itens (possívelmente de 1 até 103).
        schema:
          $ref: '#/definitions/ListOfOuterObjects'
        examples:
          rgb: ['red', 'green', 'blue']
    """

    if municipio != "favicon.ico":

        try:
            codigo_ibge = int(municipio)
        except ValueError:
            codigo_ibge = obter_codigo_ibge_pelo_nome(municipio)

        if codigo_ibge is None or not is_valid_ibge_code(codigo_ibge):
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

        municipio = get_municipio_pelo_codigo_ibge(codigo_ibge)
        resultado = procurar_resultado(municipio.id)
        return jsonify(resultado)


@api_de_resultados.route('/<municipio>/<item_id>', methods=['GET'])
def getItem(municipio, item_id):
    """Consulta de um item específico de um municipio.
    Este endpoint permite consulta o resultado da validação de um município com base no seu código IBGE.

    1. Se o código IBGE for inválido ou não for encontrado, retorna uma resposta JSON informando que o município não está disponível.
    2. Caso contrário, obtém o objeto do município correspondente ao código IBGE.
    3. Realiza uma busca por um resultado relacionado ao município.
    4. Retorna uma resposta JSON contendo o resultado encontrado para o item específico.
    
    O código lida com a entrada do usuário, verifica se é um código IBGE válido ou um nome de município. Em seguida, busca o resultado correspondente ao município/item e retorna como resposta JSON.
    
    ---
    tags:
      - Resultados
    parameters:
      - name: municipio
        in: path
        type: string
        required: true
        description: ID do municipio (código IBGE).
        parameters:
      - name: item_id
        in: path
        type: string
        required: true
        description: ID do item (1 até 103).

    responses:
      200:
        description: Obejto no formato `JSON` que contém um objeto com a resposta para o item.
        schema:
          $ref: '#/definitions/OuterObject'
        examples:
          rgb: ['red', 'green', 'blue']
    """

    try:
        codigo_ibge = int(municipio)
    except ValueError:
        codigo_ibge = obter_codigo_ibge_pelo_nome(municipio)

    if codigo_ibge is None:
        return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

    municipio = get_municipio_pelo_codigo_ibge(codigo_ibge)
    resultado = procurar_resultado(municipio.id, item_id)
    if resultado is None:
        return jsonify(Resposta.ITEM_NAO_DISPONIVEL.to_dict())
    else:
        return jsonify(resultado)


#  Usado durante o processo de migração do banco integrado SQlite par PostgreSQL
@api_de_resultados.route('/gerar_csv', methods=['GET'])
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
