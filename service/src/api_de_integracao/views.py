import json
from flask import jsonify
from flask import Blueprint
from src.empresa.manage import get_template
from src.municipio.models import Municipio
from src.checklist.manage import get_sub_tag_itens, get_tag_itens, get_tag_by_name_in_github
from src.api_de_integracao.manage import get_github_token, get_resposta_por_erro_de_coleta, is_issue_erro, salvar_resultado, formatar_nome
from src.municipio.manage_municipios import obter_codigo_ibge_pelo_nome

from src.api_de_integracao.scrip_indexar_arquivos_mp import scrip_indexar_arquivos_mp

from src.api_de_integracao.models import Resultado
from src.api_de_integracao.resposta import Resposta

api_de_integracao = Blueprint('api_de_integracao', __name__)

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