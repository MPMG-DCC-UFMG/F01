import json
from github import Github
from flask import jsonify
from flask import Blueprint
from src.checklist.manage import get_sub_tag_itens, get_tag_itens, get_tag_by_name_in_github
from src.empresa.models import Empresa
from src.empresa.manage import get_template
from src.municipio.models import Municipio
from src.api_de_integracao.manage_resultado import get_resposta_por_erro_de_coleta, is_issue_erro, salvar_resultado, formatar_nome
from src.municipio.manage_municipios import obter_codigo_ibge_pelo_nome


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

    g = Github("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")
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
        print(nome_da_tag, sub_tag, erro_de_coleta)

        if (sub_tag == None):
            itens = get_tag_itens(nome_da_tag)
        else:
            itens = get_sub_tag_itens(nome_da_sub_tag)

        for municipio in template.municipios:
            codigo_ibge = obter_codigo_ibge_pelo_nome(municipio.nome_formatado)
            for item in itens:
                salvar_resultado(municipio_id=codigo_ibge, item_id=item.id,
                                 codigo_resposta=resposta.get_codigo_resposta(), justificativa=resposta.get_justificativa())

    return jsonify('ok')
