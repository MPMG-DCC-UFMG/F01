from flask import jsonify
from flask import Blueprint
from src.municipio.manage import carregar_municipios, get_codigo_ibge_pelo_id

municipio = Blueprint('municipio', __name__, template_folder="templates")

@municipio.route('/cadastrar_municipios', methods=['GET'])
def cadastrar():
    """Cadastrar Municípios
    Este endpoint carrega os municípios a partir de dois arquivos CSV e insere-os no banco de dados.
    
    O arquivo `links_validados.csv` deve conter os links validados e seguir o seguinte formato:
    
    | Município        | Site Prefeitura                     | Portal da Transparência (validado) |
    | Belo Horizonte   | https://www.pbh.gov.br             | https://www.transparencia.pbh.gov.br |
    | Uberlândia       | https://www.uberlandia.mg.gov.br   | https://www.transparencia.uberlandia.mg.gov.br |
    
    
    O arquivo `lista_municipios.csv` deve conter os nomes dos municípios e seus códigos IBGE correspondentes, 
    e seguir o seguinte formato

    | nome            | id      |
    | Belo Horizonte  | 3106200 |
    | Uberlândia      | 3170206 |
    
    Ambos os arquivos CSV devem estar localizados no mesmo diretório deste script.
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

    try:
      carregar_municipios()
      return jsonify('ok')
    except:
      return jsonify('fail')
    


@municipio.route('/obter_municipio/<string:id_municipio>', methods=['GET'])
def obter_municipio(id_municipio):
  municipio = get_codigo_ibge_pelo_id(id_municipio)
  return jsonify(municipio.nome, ("id_ibge", municipio.id_ibge))