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


@api_de_integracao.route('/')
def index():
    return jsonify('Api de integracao ok')


# Carregar os resultado da pasta results - Não será mais utilizado!!
@api_de_integracao.route('/carregar_resultados', methods=['GET'])
def carregarResultados():

    municipios = Municipio.query.all()
    count = 0
    for municipio in municipios:

        nome_formatado = formatar_nome(municipio.nome)
        codigo_ibge = obter_codigo_ibge_pelo_nome(nome_formatado)

        try:
            with open('../results/' + nome_formatado + '.json', 'r') as myfile:
                data = myfile.read()
                resultados_do_municipio = json.loads(data)
                for item_id in resultados_do_municipio:
                    count += 1
                    salvar_resultado(
                        resultado=resultados_do_municipio[item_id], municipio_id=codigo_ibge, item_id=item_id)

        except FileNotFoundError:
            pass

    return jsonify([count])

# Indexar todos os arquivos de um template no elasticsearch usando o fscrawler
@api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>', methods=['GET'])
def indexarArquivosTemplate(nome_do_template):
    # TEMPLATES = ["siplanweb", "sintese", "abo", "betha_26", "pt_45", "memory_66", "template1_22"]
    scrip_indexar_arquivos_mp(nome_do_template)
    return jsonify('ok')


# Indexar todos os arquivos de uma tag no elasticsearch usando o fscrawler
@api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>/<string:nome_da_tag>', methods=['GET'])
def indexarArquivosTagTemplate(nome_do_template, nome_da_tag):
    # TEMPLATES = ["siplanweb", "sintese", "abo", "betha_26", "pt_45", "memory_66", "template1_22"]
    scrip_indexar_arquivos_mp(nome_do_template, nome_da_tag)
    return jsonify('ok')

@api_de_integracao.route('/indexar_arquivos', methods=['GET'])
def indexarArquivos():
    # TEMPLATES = ["portaltp_61", "pt_45", "abo_21", "grp_27"]
    TEMPLATES = ["adpm_22", "betha_26", "memory_66", "municipal_net_11", "portal_facil_60",
    "portal_facil_46", "siplanweb_61", "sintese_tecnologia_e_informatica_88", "template1_22",
    "adpm_7", "template2_28"]
    for template in TEMPLATES:
        scrip_indexar_arquivos_mp(template)
    return jsonify('templates indexados')


# Mudar de TRUE e FALSE para OK_VALIDADO e ERRO_VALIDADO

@api_de_integracao.route('/ajuste_resultados', methods=['GET'])
def ajustarResultados():

    todos_true = Resultado.query.filter_by(
        codigo_resposta="OK_VALIDADO").all()

    for resultado in todos_true:
        resposta = Resposta.OK_VALIDADO
        salvar_resultado(municipio_id=resultado.municipio_id,
                                 item_id=resultado.item_id, resposta=resposta)

    todos_false = Resultado.query.filter_by(
        codigo_resposta="ERRO_VALIDADO").all()

    for resultado in todos_false:
        resposta = Resposta.ERRO_VALIDADO
        salvar_resultado(municipio_id=resultado.municipio_id,
                                 item_id=resultado.item_id, resposta=resposta)

    return jsonify('ok')    


@api_de_integracao.route('/teste', methods=['GET'])
def testeBD():
    return jsonify('teste ok') 
