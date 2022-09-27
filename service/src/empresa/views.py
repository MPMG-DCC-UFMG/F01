import os
from src import db
import pandas as pd
from flask import jsonify
from flask import Blueprint
from src.empresa.models import Empresa
from src.municipio.models import Municipio
from src.api_de_integracao.manage import formatar_nome

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