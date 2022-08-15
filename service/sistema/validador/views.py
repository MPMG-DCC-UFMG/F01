from flask import Blueprint, render_template, request, redirect, url_for
from sistema import db
from sistema.empresa.models import Empresa
from sistema.municipio.models import Municipio

validador = Blueprint('validador', __name__, template_folder="templates")

@validador.route('/')
def index():
    empresas = Empresa.query.all()
    municipios = Municipio.query.all()

    valor_total = 0
    lucro = 0
    n_empresas = 0
    nomes = []
    for empresa in empresas:
        # valor_total = valor_total + empresa.valor_liquido
        nomes.append(empresa.nome)
        n_empresas = n_empresas + 1
        # if empresa.valor_liquido > 0:
            # lucro = lucro + 1

    prejuizo = n_empresas - lucro
    return render_template('validador.html',
                           segment='validador')