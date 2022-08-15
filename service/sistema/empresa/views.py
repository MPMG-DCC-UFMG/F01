from flask import Blueprint, render_template, request, redirect, url_for
from sistema import db
from sistema.empresa.models import Empresa
from sistema.municipio.models import Municipio

empresa = Blueprint('empresa', __name__, template_folder="templates")

@empresa.route('/')
def index():
    empresas = Empresa.query.all()
    municipios = Municipio.query.all()

    valor_total = 0
    lucro = 0
    quantidade = 0
    nomes = []
    for empresa in empresas:
        nomes.append(empresa.nome)
        quantidade = quantidade + 1

    prejuizo = quantidade - lucro
    return render_template('empresa.html',
                           empresas=empresas,
                           municipios=municipios,
                           segment='empresa',
                           valor_total=valor_total,
                           lucro=lucro,
                           quantidade=quantidade,
                           nomes=nomes)


@empresa.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():

    municipios = Municipio.query.all()
    if request.method == "POST":
        nome = request.form['nome']

        empresa = Empresa(nome=nome)
        db.session.add(empresa)


        db.session.commit()

        return redirect(
            url_for('empresa.perfil', _id_empresa=empresa.id))
    return render_template('cadastrar_empresa.html',
                           municipios=municipios,
                           segment='empresa')


@empresa.route('/editar/<int:_id_empresa>', methods=['POST', 'GET'])
def editar_empresa(_id_empresa):

    municipios = Municipio.query.all()
    empresa = Empresa.query.get_or_404(_id_empresa)

    if request.method == 'POST':
        nome = request.form['nome']

        empresa.nome = nome

        db.session.commit()

        return redirect(
            url_for('empresa.perfil', _id_empresa=empresa.id))

    return render_template('editar_empresa.html',
                           empresa=empresa,
                           segment='empresa',
                           municipios=municipios)


@empresa.route('/excluir/<int:_id_empresa>', methods=['POST', 'GET'])
def excluir_empresa(_id_empresa):
    empresa = Empresa.query.get_or_404(_id_empresa)

    if request.method == 'POST':
        db.session.delete(empresa)
        db.session.commit()

        return redirect(url_for('empresa.index'))

    return render_template('excluir_empresa.html',
                           segment='empresa',
                           empresa=empresa)


@empresa.route('/perfil/<int:_id_empresa>')
def perfil(_id_empresa):

    empresa = Empresa.query.get_or_404(_id_empresa)

    n_cidadaos = 0
    media = 0

    if n_cidadaos > 0:
        media = media / n_cidadaos
        media = round(media, 1)
    return render_template('perfil_empresa.html',
                           empresa=empresa,
                           segment='empresa',
                           media=media)


@empresa.route('/associar_cidadao/<int:_id_empresa>',
                  methods=['POST', 'GET'])
def associar_cidadao(_id_empresa):
    empresa = Empresa.query.get_or_404(_id_empresa)
    municipios = Municipio.query.all()

    if request.method == 'POST':

        id_cidadaos = request.form['municipios']
        for id_cidadao in id_cidadaos:
            municipio = Municipio.query.get_or_404(id_cidadao)
            empresa.municipios.append(municipio)
            db.session.commit()

        return redirect(
            url_for('empresa.perfil', _id_empresa=empresa.id))

    return render_template('associar_cidadao.html',
                           municipios=municipios,
                           segment='empresa',
                           empresa=empresa)


@empresa.route('/remover/<int:_id_empresa>/<int:_id_cidadao>',
                  methods=['POST', 'GET'])
def remover(_id_empresa, _id_cidadao):
    empresa = Empresa.query.get_or_404(_id_empresa)
    municipio = Municipio.query.get_or_404(_id_cidadao)

    if request.method == 'POST':
        municipio = Municipio.query.get_or_404(municipio.id)
        municipio.empresa = []
        db.session.commit()

        return redirect(
            url_for('empresa.perfil', _id_empresa=empresa.id))

    return render_template('remover_da_empresa.html',
                           municipio=municipio,
                           segment='empresa',
                           empresa=empresa)
