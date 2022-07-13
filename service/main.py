from flask import Flask
from flask import jsonify
import json
import pandas as pd
import json
from enum import Enum
app = Flask(__name__)

class Resposta(Enum):
    OK                       = 1  # Encontrado item no site
    ITEM_NAO_DISPONIVEL      = 2  # Erro genérico: não coletado
    MUNICIPIO_NAO_DISPONIVEL = 3  # Municipio não coletado
    NAO_ENCONTRADO           = 4  # Item não encontrado no portal de transparencia
    ERRO_TIMEOUT             = 5  # Item encontrado, mas houve erro de timeout na coleta

    def __str__(self):
        return (self.name)

def open_file(municipio):

    # consulta por id do municipio
    try:
        id = int(municipio)
        try:
            municipio = df.loc[id]['api']
        except KeyError:
            return str(Resposta.MUNICIPIO_NAO_DISPONIVEL)
    except ValueError:
        pass

    # consulta por nome do municipio
    try:
        with open(PATH_RESULTS_BASE + municipio +'.json', 'r') as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return obj

    except FileNotFoundError:
        return str(Resposta.MUNICIPIO_NAO_DISPONIVEL)

@app.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":
        obj = open_file(municipio)
        return jsonify(obj)

    return jsonify(str(Resposta.MUNICIPIO_NAO_DISPONIVEL))

@app.route('/<municipio>/<item>',methods=['GET'])
def getItem(municipio, item):

    obj = open_file(municipio)

    if item in obj:
        return jsonify(obj[item])
    else:
        return jsonify(str(Resposta.ITEM_NAO_DISPONIVEL))


PATH_RESULTS_BASE = '/dados01/workspace/ufmg_2021_f01/ufmg.amedeiros/F01/results/'
# PATH_RESULTS_BASE = '../results/'

app.run(debug=True)
df = pd.read_csv("../lista_municipios.csv")
df.set_index('id', inplace = True)
