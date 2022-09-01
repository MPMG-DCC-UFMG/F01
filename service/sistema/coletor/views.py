import json
from sistema import db
from github import Github
from sistema.empresa.models import Empresa
from sistema.municipio.models import Municipio
from sistema.coletor.models import Coletor
from flask import Blueprint, render_template, request, redirect, url_for

coletor = Blueprint('coletor', __name__, template_folder="templates")

@coletor.route('/')
def index():
    empresas = Empresa.query.all()
    municipios = Municipio.query.all()
    coletores = Coletor.query.all()

    return render_template('coletor.html',
                           empresas=empresas,
                           municipios=municipios,
                           coletores=coletores,
                           segment='empresa')


@coletor.route('/sincronizar')
def sincronizar():
    empresas = Empresa.query.all()
    municipios = Municipio.query.all()

    # SINCRONIZAR ISSUES GITHUB
    g = Github("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")
    repo = g.get_repo("MPMG-DCC-UFMG/F01")

    label_epic = repo.get_label('Epic')
    label_realizacaof01 = repo.get_label('Realização F01')
    issues = repo.get_issues(state='all',sort='created', direction='asc', labels=[label_epic, label_realizacaof01])

    print("label tag-servidores:")
    print(issues)
    for iss in issues:
        print(iss, iss.state)
        empresa = Coletor(nome=iss.title)
        db.session.add(empresa)

    db.session.commit()

    return redirect(url_for('coletor.index'))


@coletor.route('/excluir_coletores')
def excluir_coletores():
    coletores = Coletor.query.all()

    for coletor in coletores:
        db.session.delete(coletor)
    db.session.commit()
    
    return redirect(url_for('coletor.index'))
