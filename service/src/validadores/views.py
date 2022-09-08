from src import db
from flask import jsonify
from flask import Blueprint

validadores = Blueprint('validadores', __name__)


@validadores.route('/')
def index():

    return jsonify('Validadores.')