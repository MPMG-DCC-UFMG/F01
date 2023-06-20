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


# Indexar todos os arquivos de um template no elasticsearch usando o fscrawler
#  Executa o script para indexar arquivos de um template específico no Elasticsearch usando o fscrawler.
@api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>', methods=['GET'])
def indexarArquivosTemplate(nome_do_template):
    """Indexar arquivos pelo nome do template
    Este endpoint permite indexar arquivos com base no nome do template.
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