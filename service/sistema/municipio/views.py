import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from sistema import db
from sistema.municipio.models import Municipio
from sistema.empresa.models import Empresa

municipio = Blueprint('municipio', __name__, template_folder="templates")

@municipio.route('/')
def index():
    municipios = Municipio.query.all()

    soma = 0
    n_cidadaos = 0
    baixo = 0
    media = 0
    n_marcados = 0
    # for municipio in municipios:
        # media = media + municipio.felicidade
        # n_cidadaos = n_cidadaos + 1
        # if municipio.felicidade < 8:
            # municipio.marcado = 1
            # baixo = baixo + 1
            # db.session.commit()
        # if municipio.marcado == 1:
            # n_marcados = n_marcados + 1

    if n_cidadaos > 0:
        media = media / n_cidadaos
        media = round(media, 1)

    return render_template('municipio.html',
                           municipios=municipios,
                           segment='municipio',
                           media=media,
                           n_cidadaos=n_cidadaos,
                           baixo=baixo,
                           n_marcados=n_marcados)


@municipio.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    if request.method == "POST":
        nome = request.form['nome']

        municipio = Municipio(nome=nome)
        db.session.add(municipio)
        db.session.commit()

        return redirect(url_for('municipio.index'))
    return render_template(
        'cadastrar_municipio.html',
        segment='municipio',
    )


@municipio.route('/editar/<int:_id>', methods=['GET', 'POST'])
def editar_municipio(_id):
    municipio = Municipio.query.get_or_404(_id)

    if request.method == 'POST':
        nome = request.form['nome']

        municipio.nome = nome
        # if felicidade != '11':
        #     municipio.felicidade = felicidade

        db.session.commit()

        return redirect(url_for('municipio.perfil', _id=municipio.id))

    return render_template('editar_municipio.html',
                           segment='municipio',
                           municipio=municipio)


@municipio.route('/excluir/<int:_id>', methods=['POST', 'GET'])
def excluir_municipio(_id):
    municipio = Municipio.query.get_or_404(_id)

    if request.method == 'POST':
        db.session.delete(municipio)
        db.session.commit()

        return redirect(url_for('municipio.index'))

    return render_template('excluir_municipio.html',
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


@municipio.route('/perfil/<int:_id>', methods=['POST', 'GET'])
def perfil(_id):
    municipio = Municipio.query.get_or_404(_id)

    if request.method == 'POST':
        marcado = request.form['marcado']
        if marcado == 'Marcar':
            municipio.marcado = 1
            db.session.commit()
        if marcado == 'Desmarcar':
            municipio.marcado = 0
            db.session.commit()

        return redirect(url_for('municipio.perfil', _id=municipio.id))

    return render_template('perfil_municipio.html',
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
