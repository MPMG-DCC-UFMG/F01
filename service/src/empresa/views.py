import os
import json 
from src import db
import pandas as pd
from flask import jsonify
from flask import Blueprint
from src.empresa.models import Empresa
from src.municipio.models import Municipio
from src.api_de_integracao.manage import formatar_nome
from src.empresa.manage import get_nome_dos_municipios_do_template_sem_formatar

empresa = Blueprint('empresa', __name__, template_folder="templates")


@empresa.route('/')
def index():
    templates = Empresa.query.all()
    if len(templates):
        templates = [template.nome for template in templates]
    # municipios = Municipio.query.all()

    print(templates)
    return jsonify(templates)


@empresa.route('/cadastrar_templates', methods=['POST', 'GET'])
def cadastrar():

    Empresa.query.delete()

    # 1) Insere os templates unicos do csv 'municipios_clusters' na tabela de templates

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/municipios_clusters.csv')

    nomes = df['template_name_size'].unique()

    for nome in nomes:
        if (pd.isna(nome)):
            nome = 'sem_template'
        nome = formatar_nome(nome)
        empresa = Empresa(nome=formatar_nome(nome))
        db.session.add(empresa)
    db.session.commit()

    # 2) Para cada municipio, associa o template.

    for _, row in df.iterrows():
        nome_do_municipio = row['municipio']
        nome_da_empresa = row['template_name_size']

        if (pd.isna(nome_da_empresa)):
            nome_da_empresa = 'sem_template'
        nome_da_empresa = formatar_nome(nome_da_empresa)

        municipio = Municipio.query.filter_by(nome=nome_do_municipio).all()[0]
        if (len(municipio.empresa) == 0):
            empresa = Empresa.query.filter_by(nome=nome_da_empresa).all()[0]
            municipio.empresa.append(empresa)

    db.session.commit()

    return jsonify('ok')


@empresa.route('/<string:nome_do_template>', methods=['POST', 'GET'])
def municipios_do_template(nome_do_template):
    return jsonify(get_nome_dos_municipios_do_template_sem_formatar(nome_do_template))


# Gerar jsons com os nomes de múnicipios de cara template. Usado no gerador de issues
@empresa.route('/gerar_jsons', methods=['POST', 'GET'])
def gerar_jsons():
    templates = Empresa.query.all()
    if len(templates):
        templates = [template.nome for template in templates]
    for nome_do_template in templates:
        with open(os.getcwd() + f"/src/empresa/municipios/{nome_do_template}.json", "w", encoding = "utf-8") as outfile: 
            print(get_nome_dos_municipios_do_template_sem_formatar(nome_do_template))
            json_object = json.dumps(get_nome_dos_municipios_do_template_sem_formatar(nome_do_template), indent = 4, ensure_ascii = False) 
            outfile.write(json_object) 

    return jsonify('ok') 

