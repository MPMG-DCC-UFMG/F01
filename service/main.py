from flask import Flask
from flask import jsonify
import json
import pandas as pd
app = Flask(__name__)
app.run(debug=True)

import json

df = pd.read_csv("../lista_municipios.csv")
df.set_index('id', inplace = True)

PATH_RESULTS_BASE = '/dados01/workspace/ufmg_2021_f01/ufmg.amedeiros/F01/results/'
# PATH_RESULTS_BASE = '../results/'

def open_file(namefile):
    try:
        id = int(namefile)
        try:
            namefile = df.loc[id]['api']
        except KeyError:
            pass
    except ValueError:
        pass

    try:
        with open(PATH_RESULTS_BASE + namefile +'.json', 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        return obj

    except FileNotFoundError:
        return "Municipio nao disponivel ou encontrado"

@app.route('/<municipio>', methods=['GET'])
def getAllItens(municipio):

    if municipio != "favicon.ico":

        obj = open_file(municipio)
        return jsonify(obj)

    return jsonify("Municipio nao disponivel ou encontrado")

@app.route('/<municipio>/<item>',methods=['GET'])
def getItem(municipio, item):

    obj = open_file(municipio)

    if item in obj:
        return jsonify(obj[item])
    else:
        return jsonify("Nao disponivel")



    
