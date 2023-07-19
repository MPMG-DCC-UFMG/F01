from flask import jsonify
from flask import Blueprint
from flask import redirect
import pandas as pd
from src import db
import numpy as np
import os
from src.checklist.manage import get_all_itens
from src.api_de_integracao.manage import procurar_resultado
from src.municipio.manage import get_all_municipios
from src.empresa.manage import get_all_templates
from src.api_de_integracao.models import Resultado

from src.api_de_integracao.scrip_indexar_arquivos_mp import scrip_indexar_arquivos_mp

api_de_integracao = Blueprint('api_de_integracao', __name__)

@api_de_integracao.route("/")
def hello_world():
    return redirect('/apidocs')

@api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>', methods=['GET'])
def indexarArquivosTemplate(nome_do_template):
    """Indexar arquivos pelo nome do template
    Este endpoint permite indexar arquivos com base no nome do template. Executa o script para indexar arquivos de um template específico no **Elasticsearch** usando o **fscrawler**.
    
    Esse código executa uma função chamada scrip_indexar_arquivos_mp que tem a finalidade de indexar arquivos de um template específico no **Elasticsearch** usando o **fscrawler**. Vou explicar as partes principais do código:

    1. O código obtém uma lista de municípios relacionados ao template fornecido usando a função `get_municipios_do_template(nome_do_template)`. Os municípios são armazenados na variável `MUNICIPIOS`.
    
    2. O código entra em um loop que percorre cada município da lista `MUNICIPIOS`.
    
    3. Em seguida, o código define um dicionário chamado ``config`` que contém várias configurações relacionadas à indexação de arquivos usando o **fscrawler**. As configurações incluem informações sobre o local dos arquivos a serem indexados, configurações do **Elasticsearch** e configurações específicas do **fscrawler**.
    
    4. O código verifica se o diretório *municipio_directory* já existe. Se existir, verifica se um arquivo de configuração `_settings.yaml` também existe. Se o arquivo de configuração existir, exibe uma mensagem informando que o arquivo de configuração já existe. Caso contrário, o código cria o arquivo de configuração e o preenche com as configurações contidas no dicionário ``config``.
    
    5. Se o diretório *municipio_directory* não existir, o código cria o diretório e em seguida cria o arquivo de configuração `_settings.yaml`, preenchendo-o com as configurações contidas no dicionário ``config``.
    
    6. Após a criação do arquivo de configuração, o código executa o **fscrawler** para iniciar o processo de indexação dos arquivos. Isso é feito usando a biblioteca *subprocess* para executar o comando do **fscrawler** como um processo separado.
    
    7. O código captura a saída do processo do **fscrawler** e exibe mensagens indicando se o processo foi concluído com êxito ou se foi encerrado devido a um limite de tempo *(TIME_OUT)*.
    
    8. Por fim, o código verifica se um arquivo `_status.json` foi gerado durante o processo de indexação. Se o arquivo existir, ele é aberto e o seu conteúdo é exibido.

    ---
    tags:
      - Indexação de Arquivos
    parameters:
      - name: nome_do_template
        in: path
        type: string
        required: true
        description: Nome do template para indexação dos arquivos
    responses:
      200:
        description: Sucesso na indexação dos arquivos
        schema:
          type: string
          example: 'ok'
    """
    scrip_indexar_arquivos_mp(nome_do_template)
    return jsonify('ok')


# # Indexar todos os arquivos de uma tag no elasticsearch usando o fscrawler
# @api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>/<string:nome_da_tag>', methods=['GET'])
# def indexarArquivosTagTemplate(nome_do_template, nome_da_tag):
#     scrip_indexar_arquivos_mp(nome_do_template, nome_da_tag)
#     return jsonify('ok')

# @api_de_integracao.route('/indexar_arquivos', methods=['GET'])
# def indexarArquivos():
#     # TEMPLATES = ["portaltp_61", "pt_45", "abo_21", "grp_27"]
#     TEMPLATES = ["adpm_22", "betha_26", "memory_66", "municipal_net_11", "portal_facil_60",
#     "portal_facil_46", "siplanweb_61", "sintese_tecnologia_e_informatica_88", "template1_22",
#     "adpm_7", "template2_28"]
#     for template in TEMPLATES:
#         scrip_indexar_arquivos_mp(template)
#     return jsonify('templates indexados')


@api_de_integracao.route('/gerar_csv', methods=['GET'])

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

def escrever_lista_em_arquivo(arquivo_nome, lista):
    # Abre o arquivo em modo de escrita ('w')
    with open(arquivo_nome, 'w') as arquivo:
        # Converte cada elemento da lista em uma string e, em seguida, junta-os usando '\n'
        lista_formatada = '\n'.join(str(item) for item in lista)
        # Escreve a string formatada no arquivo
        arquivo.write(lista_formatada)

def subir_resultados():
    if len(Resultado.query.all()):
        return
    print("Subindo resultados")

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Navegue dois níveis acima para chegar à pasta onde resultados.csv está localizado
    caminho_csv = os.path.join(diretorio_atual, '..', '..', 'resultados.csv')
    df = pd.read_csv(caminho_csv)
    for row in df.itertuples():
        data_validacao = row.validated_at
        if type(row.validated_at) != str:
            data_validacao = None
        novo_resultado = Resultado(item_id= row.id_item,
                                   municipio_id= row.id_municipio,
                                   codigo_resposta= row.codigo_resposta,
                                   data_validacao = data_validacao,
                                   justificativa= row.justificativa)
        db.session.add(novo_resultado)
        db.session.commit()

@api_de_integracao.route('/teste', methods=['GET'])
# Carregar banco
def teste():
  itens = get_all_itens()
  for item in itens:
      print(item.id)
  templates = get_all_templates()
  municipios = get_all_municipios()
  results = Resultado.query.all()
  print(len(itens))
  print(len(templates))
  print(len(municipios))
  print(len(results))
  return jsonify("opa")

