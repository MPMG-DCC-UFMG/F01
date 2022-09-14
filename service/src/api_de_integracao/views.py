import json
from github import Github
from flask import jsonify
from flask import Blueprint
from src.empresa.models import Empresa
from src.municipio.models import Municipio
from src.api_de_integracao.manage_resultado import salvar_resultado, formatar_nome
from src.municipio.manage_municipios import obter_codigo_ibge_pelo_nome


api_de_integracao = Blueprint('api_de_integracao', __name__)


@api_de_integracao.route('/')
def index():
    municipios = Municipio.query.all()
    empresas = Empresa.query.all()

    return jsonify('ok')


# Temporariamente da pasta results
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
    issues = repo.get_issues(state='closed',sort='created', direction='asc', labels=[label_epic, label_realizacaof01])

    tags = []

    for issue in issues:

        for label in issue.labels:
            # a = 'tag - a-b-c'
            infos = label.name.split('-')
            if infos[0] == 'tag ':
                tags.append(" ".join(infos[1:]))
    print(tags.unique())
            # if 'tag -' in label.name:
            #     print(label.name)


    # municipios = Municipio.query.all()
    # for municipio in municipios:

    #     codigo_ibge = obter_codigo_ibge_pelo_nome(nome_formatado)

        
    #     with open('../results/' + nome_formatado + '.json', 'r') as myfile:
    #         data = myfile.read()
    #         resultados_do_municipio = json.loads(data)
    #         for item_id in resultados_do_municipio:
    #             count += 1
    #             salvar_resultado(
    #                 resultado=resultados_do_municipio[item_id], municipio_id=codigo_ibge, item_id=item_id)


    return jsonify('ok')