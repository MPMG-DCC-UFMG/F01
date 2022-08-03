from flask import Flask
from flask import jsonify
import json
import pandas as pd
import json
from enum import Enum

class Resposta(Enum):
    OK                        = 0  # Item validado com sucesso
    ITEM_NAO_DISPONIVEL       = 1  # Erro generico para item
    MUNICIPIO_NAO_DISPONIVEL  = 2  # Erro generico para municipio
    NAO_COLETADO              = 3  # Item nao encontrado no portal de transparencia
    NAO_COLETADO_ERRO_TIMEOUT = 4  # Item encontrado, mas houve erro de timeout na coleta
    NAO_VALIDADO              = 5  # Validacao informou que o item coletado nao atende aos requisitos 
    
    def to_dict(self):
        return {'resposta':self.value, 'justificativa':self.name}
    
# Aplicacao
app = Flask(__name__)
df = pd.read_csv("../lista_municipios.csv")

df.set_index('id', inplace = True)
PATH_RESULTS_BASE = '/dados01/workspace/ufmg_2021_f01/ufmg.amedeiros/F01/results/'
# PATH_RESULTS_BASE = '../results/'

def open_file(municipio):

    # consulta por id do municipio
    try:
        id = int(municipio)
        try:
            municipio = df.loc[id]['api']
        except KeyError:
            return Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict()
    except ValueError:
        pass

    # consulta por nome do municipio
    try:
        with open(PATH_RESULTS_BASE + municipio +'.json', 'r') as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return obj

    except FileNotFoundError:
        return Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict()

@app.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":
        obj = open_file(municipio)
        return jsonify(obj)

    return jsonify(Resposta.MUNICIPIO_NAO_DISPONIVEL.to_dict())

@app.route('/<municipio>/<item>',methods=['GET'])
def getItem(municipio, item):

    obj = open_file(municipio)

    if item in obj:
        return jsonify(obj[item])
    else:
        return jsonify(Resposta.ITEM_NAO_DISPONIVEL.to_dict())


app.run(debug=True)
