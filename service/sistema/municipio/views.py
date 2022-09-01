import os
import pandas as pd
from sistema import db
from sistema.municipio import manage
from sistema.empresa.models import Empresa
from sistema.municipio.models import Municipio
from flask import Blueprint, render_template, request, redirect, url_for, current_app

municipio = Blueprint('municipio', __name__, template_folder="templates")


@municipio.route('/')
def index():
    municipios = Municipio.query.all()

    return render_template('municipio.html',
                           municipios=municipios,
                           segment='municipio')


@municipio.route('/carregar', methods=['GET'])
def carregar():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/links_validados.csv')

    Municipio.query.delete()

    for _, row in df.iterrows():
        municipio = manage.insert_municipio(nome=row['Município'],
                                            url_site_prefeitura=row['Site Prefeitura'],
                                            url_portal=row['Portal da Transparência (validado)'])

    municipios = Municipio.query.all()

    return render_template('municipio.html',
                           municipios=municipios,
                           segment='municipio')


@municipio.route('/editar/<int:_id>', methods=['GET', 'POST'])
def editar_municipio(_id):
    municipio = Municipio.query.get_or_404(_id)

    if request.method == 'POST':
        nome = request.form['nome']

        municipio.nome = nome

        db.session.commit()

        return redirect(url_for('municipio.perfil', _id=municipio.id))

    return render_template('editar_municipio.html',
                           segment='municipio',
                           municipio=municipio)


@municipio.route('/atribuir_empresa/<int:_id>', methods=['POST', 'GET'])
def atribuir_empresa(_id):
    municipio = Municipio.query.get_or_404(_id)
    empresas = Empresa.query.all()

    if request.method == 'POST':
        id_empresa = request.form['id_empresa']
        empresa = Empresa.query.get_or_404(id_empresa)
        municipio.empresa.append(empresa)

        db.session.commit()

        return redirect(url_for('municipio.perfil', _id=municipio.id))
    return render_template('atribuir_empresa.html',
                           municipio=municipio,
                           segment='municipio',
                           empresas=empresas)

@municipio.route('/perfil/<int:_id>', methods=['GET'])
def perfil(_id):
    municipio = Municipio.query.get_or_404(_id)

    return render_template('dados_municipio.html',
                           segment='municipio',
                           municipio=municipio)


@municipio.route('/remover/<int:_id_empresa>/<int:_id_cidadao>',
                 methods=['POST', 'GET'])
def remover_empresa(_id_empresa, _id_cidadao):
    municipio = Municipio.query.get_or_404(_id_cidadao)
    empresa = Empresa.query.get_or_404(_id_empresa)

    if request.method == 'POST':
        municipio = Municipio.query.get_or_404(municipio.id)
        municipio.empresa = []
        db.session.commit()

        return redirect(url_for('municipio.perfil', _id=municipio.id))

    return render_template('remover_empresa.html',
                           municipio=municipio,
                           segment='municipio',
                           empresa=empresa)
