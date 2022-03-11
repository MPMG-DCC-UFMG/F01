from flask import Flask
from flask import jsonify
import json
app = Flask(__name__)
app.run(debug=True)

PATH_RESULTS_BASE = '/dados01/workspace/ufmg_2021_f01/ufmg.amedeiros/F01/results/'

def open_file(namefile):
    with open(PATH_RESULTS_BASE + namefile +'.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    return obj

@app.route('/<municipio>',methods=['GET'])
def getAllItens(municipio):
    try:
        obj = open_file(municipio)
        return jsonify(obj)
    except FileNotFoundError:
        return jsonify("Nao disponivel")
        

@app.route('/<municipio>/<item>',methods=['GET'])
def getItem(municipio, item):
    obj = open_file(municipio)
    print(municipio)
    if item in obj:
        return jsonify(obj[item])
    else:
        return jsonify("Nao disponivel")
