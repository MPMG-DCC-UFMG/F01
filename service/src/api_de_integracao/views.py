import json
from github import Github
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
    return jsonify('ok')


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


@api_de_integracao.route('/carregar_resultados_github', methods=['GET'])
def carregarResultadosGithub():

    g = Github(get_github_token())
    repo = g.get_repo("MPMG-DCC-UFMG/F01")

    label_epic = repo.get_label('Epic')
    label_realizacaof01 = repo.get_label('Realização F01')
    issues = repo.get_issues(state='closed', sort='created', direction='asc', labels=[
                             label_epic, label_realizacaof01])

    # Como no github temos um "-" separando o que é label, por exemplo
    # template - Betha, tag - despesas
    # No código abaixo que vai ler as labels chamamos o que está antes de "-" de select e depois de informação

    for issue in issues:
        template = None
        erro_de_coleta = None
        nome_da_tag = None
        sub_tag = None

        for label in issue.labels:

            infos = label.name.split('-')
            select = infos[0]
            informacao = formatar_nome(" ".join(infos[1:]))

            if (is_issue_erro(label.name)):
                erro_de_coleta = label.name

            elif select == 'template ':
                template = get_template(nome_do_template=informacao)

            elif select == 'tag ':
                nome_da_tag = informacao

            elif select == 'subtag ':
                nome_da_sub_tag = informacao

        if (erro_de_coleta == None):
            continue
        resposta = get_resposta_por_erro_de_coleta(erro_de_coleta)

        nome_da_tag = get_tag_by_name_in_github(nome_da_tag)
        print(issue)
        print(nome_da_tag, sub_tag, erro_de_coleta)

        if (sub_tag == None):
            itens = get_tag_itens(nome_da_tag)
        else:
            itens = get_sub_tag_itens(nome_da_sub_tag)

        for municipio in template.municipios:
            for item in itens:
                salvar_resultado(municipio_id=municipio.id, item_id=item.id,resposta=resposta)

    return jsonify('ok')

# Indexar os arquivos no elasticsearch usando o fscrawler
@api_de_integracao.route('/indexar_arquivos/<string:nome_do_template>', methods=['GET'])
def indexarArquivosTemplate(nome_do_template):
    # TEMPLATES = ["siplanweb", "sintese", "abo", "betha_26", "pt_45", "memory_66", "template1_22"]
    scrip_indexar_arquivos_mp(nome_do_template)
    return jsonify('ok')

@api_de_integracao.route('/indexar_arquivos', methods=['GET'])
def indexarArquivos():
    TEMPLATES = ["portaltp_61", "pt_45", "abo_21", "grp_27"]
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