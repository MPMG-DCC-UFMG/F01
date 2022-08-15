from flask import Blueprint, render_template
from sistema.municipio.models import Municipio
from sistema.empresa.models import Empresa
from sistema import db

principal = Blueprint('principal', __name__)


@principal.route('/')
def index():
    municipios = Municipio.query.all()
    empresas = Empresa.query.all()

    valor_total = 0
    lucro = 0
    n_empresas = 0
    for empresa in empresas:

        # valor_total = valor_total + empresa.valor_liquido
        n_empresas = n_empresas + 1
        # if empresa.valor_liquido > 0:
            # lucro = lucro + 1

    n_cidadaos = 0
    baixo = 0
    media = 0
    for municipio in municipios:
        # media = media + municipio.felicidade
        n_cidadaos = n_cidadaos + 1
        # if municipio.felicidade <= 8:
        #     municipio.marcado = 1
        #     baixo = baixo + 1
        #     db.session.commit()
        # elif municipio.felicidade > 8:
        #     municipio.marcado = 0
        #     db.session.commit()

    if n_cidadaos > 0:
        media = media / n_cidadaos
        media = round(media, 1)

    return render_template("home.html",
                           municipios=municipios,
                           empresas=empresas,
                           segment='index',
                           media=media,
                           n_empresas=n_empresas,
                           n_cidadaos=n_cidadaos,
                           valor_total=valor_total)
