from flask import jsonify
from flask import Blueprint
from enum import Enum

from src.api_de_resultados.models import Resultado, Municipio, Empresa
from src.api_de_resultados.manage import get_municipio_pelo_codigo_ibge, is_valid_ibge_code, obter_codigo_ibge_pelo_nome

api_de_resultados = Blueprint(
    'api_de_resultados', __name__)

class Resposta(Enum):
    # "Name" sera' o código e "Value" a justificativa

    # Validação
    ITEM_NAO_DISPONIVEL = "Item ainda nao validado"

    ERRO_VALIDADO = "Validacao informou que o item coletado nao atende aos requisitos"
    OK_VALIDADO = "Item validado com sucesso"

    MUNICIPIO_NAO_VALIDADO = "Municipio ainda nao validado"

    # Outros erros
    MUNICIPIO_NAO_DISPONIVEL = "Municipio invalido ou nao abordado"

    def to_dict(self):
        try:
            return {'codigo': self.name, 'justificativa': self.value + ". " + self.explain}
        except AttributeError:
            return {'codigo': self.name, 'justificativa': self.value}

    def get_codigo_resposta(self):
        return self.name
  
    def get_justificativa(self):
        try:
            return self.value  + ". " +  self.explain
        except AttributeError:
            return self.value

    def set_justificativa(self, justificativa):
        self.explain = justificativa

def procurar_resultado(municipio_id, item_id=None):

    # Retorna todos os resultados do mesmo município
    if item_id is None:
        resultado = [
            {resultado.item_id: {
                'codigo_resposta': resultado.codigo_resposta,
                'validated_at': resultado.data_validacao,
                'justificativa': resultado.justificativa}
             }
            for resultado in Resultado.query.filter_by(municipio_id=municipio_id).all()
        ]

        return resultado

    resultado = Resultado.query.filter_by(
        municipio_id=municipio_id, item_id=item_id).first()

    if resultado is not None:

        resultado = {resultado.item_id: {
            'codigo_resposta': resultado.codigo_resposta,
            'validated_at': resultado.data_validacao,
            'justificativa': resultado.justificativa}
        }

    return resultado

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
        if municipio is None:
            return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())
        resultado = procurar_resultado(municipio.id)
        if not len(resultado):
            return jsonify(Resposta.MUNICIPIO_NAO_VALIDADO.to_dict())

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
  

@api_de_resultados.route('/', methods=['GET'])
def index():
    return jsonify('Api de resultados ok')
  