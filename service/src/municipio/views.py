import os
import pandas as pd
from flask import jsonify
from src.municipio import manage_municipios
from src.municipio.models import Municipio
from flask import Blueprint
from src.api_de_integracao.manage import formatar_nome

municipio = Blueprint('municipio', __name__, template_folder="templates")

@municipio.route('/carregar_municipios', methods=['GET'])
def carregar():
    """Carregar Municípios
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/links_validados.csv')

    Municipio.query.delete()

    # Coloca o id_ibge com base na lista_municipios.csv
    codigos_ibge = []
    df_municipios = pd.read_csv(dir_path + '/lista_municipios.csv', index_col='nome')

    for _, row in df.iterrows():
        nome_do_municipio = row['Município']
        municipio_com_codigo = df_municipios.loc[nome_do_municipio]
        codigo_ibge_do_municipio = municipio_com_codigo['id']
        codigos_ibge.append(municipio_com_codigo['id']) 

        nome_formatado = formatar_nome(row['Município']) 

        municipio = manage_municipios.inserir_municipios(nome=row['Município'],
                                            nome_formatado=nome_formatado,
                                            url_site_prefeitura=row['Site Prefeitura'],
                                            url_portal=row['Portal da Transparência (validado)'],
                                            id_ibge=int(codigo_ibge_do_municipio))

    df['id_ibge'] = codigos_ibge
    df.to_csv(dir_path + '/links_validados.csv', index=False)

    return jsonify('ok')
