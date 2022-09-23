import os
import pandas as pd
from flask import jsonify
from src.municipio import manage_municipios
from src.municipio.models import Municipio
from flask import Blueprint, render_template
from src.api_de_integracao.manage import formatar_nome

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

        nome_formatado = formatar_nome(row['Município']) 

        municipio = manage_municipios.inserir_municipios(nome=row['Município'],
                                            nome_formatado=nome_formatado,
                                            url_site_prefeitura=row['Site Prefeitura'],
                                            url_portal=row['Portal da Transparência (validado)'],
                                            id_ibge=int(codigo_ibge_do_municipio))

    df['id_ibge'] = codigos_ibge
    df.to_csv(dir_path + '/links_validados.csv', index=False)

    return jsonify('ok')
