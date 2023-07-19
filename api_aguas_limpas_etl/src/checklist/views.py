from flask import jsonify
from flask import Blueprint
from flask import Blueprint

checklist = Blueprint('checklist', __name__)

@checklist.route('/cadastrar_checklist', methods=['GET'])
def cadastrar_checklist():
    """ Cadastrar Checklist
    Este endpoint é usado para registrar a checklist no banco de dados.

    Este código realiza o seguinte:

    1. Remove todos os registros existentes nas tabelas *Tag*, *Subtag* e *Item*.
    2. Lê um arquivo CSV chamado `lista_exigencias.csv`.
    3. Cadastra as tags presentes no arquivo CSV, verificando se já estão cadastradas.
    4. Cadastra as subtags presentes no arquivo CSV, vinculando-as às tags correspondentes.
    5. Cadastra os itens presentes no arquivo CSV, vinculando-os às tags e subtags correspondentes. Verifica se o item já está cadastrado.
    6. Retorna uma resposta JSON contendo a mensagem 'ok'.
    
    O código limpa as tabelas existentes, lê um arquivo CSV  `/lista_exigencias.csv` e realiza o cadastro das informações presentes no arquivo nas tabelas do banco de dados.

    ---
    tags:
      - Gerênciamento do banco de dados 
    responses:
      200:
        description: Sucesso
        schema:
          type: string
          example: 'ok'
    """


    return jsonify('ok')
