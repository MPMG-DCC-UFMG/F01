import os
import pandas as pd
from src.municipio.manage_municipios import formatar_nome_de_municipio
from src import db
from src.municipio import manage_municipios
from src.empresa.models import Empresa
from src.municipio.models import Municipio
from flask import Blueprint, render_template, request, redirect, url_for, current_app

municipio = Blueprint('municipio', __name__, template_folder="templates")

@municipio.route('/')
def index():
    municipios = Municipio.query.all()

    return render_template('municipio.html',
                           municipios=municipios,
                           segment='municipio')


@municipio.route('/carregar_municipios', methods=['GET'])
def carregar():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/links_validados.csv')

    Municipio.query.delete()

    # Coloca o id_ibge com base na lista_municipios.csv
    codigos_ibge = []
    df_municipios = pd.read_csv(dir_path + '/lista_municipios.csv', index_col='nome')

    for _, row in df.iterrows():
        nome_do_municipio = row['Município']
        municipio_com_codigo = df_municipios.loc[nome_do_municipio]
        codigo_ibge_do_municipio = municipio_com_codigo['id']
        codigos_ibge.append(municipio_com_codigo['id']) 
        print(codigo_ibge_do_municipio)

        nome_formatado = formatar_nome_de_municipio(row['Município']) 

        municipio = manage_municipios.inserir_municipios(nome=row['Município'],
                                            nome_formatado=nome_formatado,
                                            url_site_prefeitura=row['Site Prefeitura'],
                                            url_portal=row['Portal da Transparência (validado)'],
                                            id_ibge=int(codigo_ibge_do_municipio))

    df['id_ibge'] = codigos_ibge
    df.to_csv(dir_path + '/links_validados.csv', index=False)

    municipios = Municipio.query.all()

    return render_template('municipio.html',
                           municipios=municipios,
                           segment='municipio')


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
