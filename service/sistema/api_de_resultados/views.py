from flask import Blueprint, render_template, request, redirect, url_for
from sistema import db
from sistema.empresa.models import Empresa
from sistema.municipio.models import Municipio

api = Blueprint('api', __name__, template_folder="templates")

@api.route('/')
def index():
    return render_template('api.html',
                           segment='api')