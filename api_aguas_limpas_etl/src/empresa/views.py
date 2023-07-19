import os
import json
from flask import jsonify
from flask import Blueprint
from src.empresa.models import Empresa
from src.empresa.manage import get_nome_dos_municipios_do_template_sem_formatar, get_nome_dos_templates, carregar_templates

empresa = Blueprint('empresa', __name__)

@empresa.route('/')
def index():
    templates = get_nome_dos_templates()
    return jsonify(templates)


@empresa.route('/cadastrar_templates', methods=['GET'])
def cadastrar():
    """Cadastrar Templates
    Este endpoint cadastra os templates únicos do arquivo CSV 'municipios_clusters.csv' na tabela de templates.
    
    O arquivo 'municipios_clusters.csv' deve conter as seguintes colunas:
    
    | municipio    | template_name_size |
    | Belo Horizonte | template_1        |
    | Uberlândia    | template_2        |
    
    ---
    tags:
      - Gerênciamento do banco de dados
    responses:
      200:
        description: OK
    """
    try:
      carregar_templates()
      return jsonify('ok')
    except:
      return jsonify('fail')
    

@empresa.route('/<string:nome_do_template>', methods=['GET'])
def municipios_do_template(nome_do_template):
    """Municípios do Template
    Este endpoint retorna os nomes dos municípios associados a um determinado template.    
    ---
    tags:
      - Consultas no banco de dados
    parameters:
      - name: nome_do_template
        in: path
        type: string
        required: true
        description: O nome do template a ser consultado.
        enum:
          - sintese_tecnologia_e_informatica_88
          - memory_66
          - portaltp_61
          - siplanweb_61
          - portal_facil_60
          - portal_facil_46
          - pt_45
          - template2_28
          - grp_27
          - betha_26
          - adpm_22
          - template1_22
          - abo_21
          - municipal_net_11
          - template1_9
          - adpm_7
          - betha_7
          - e-cidade_7
          - fiorilli_sociedade_civil_7
          - habeas_data_7
          - horusdm_7
          - memory_6
          - portaltransp_6
          - ipm_sistemas_5
          - municipio_web_5
          - portal_facil_5
          - tecnologia_global_sistemas_5
          - template3_5
          - dardani_sistemas_4
          - govbr_4
          - sem_template
    responses:
      200:
        description: OK
    """
    return jsonify(get_nome_dos_municipios_do_template_sem_formatar(nome_do_template))


# Gerar jsons com os nomes de múnicipios de cara template. Usado no gerador de issues
@empresa.route('/gerar_jsons', methods=['POST', 'GET'])
def gerar_jsons():
    templates = Empresa.query.all()
    if len(templates):
        templates = [template.nome for template in templates]
    for nome_do_template in templates:
        with open(os.getcwd() + f"/src/empresa/municipios/{nome_do_template}.json", "w", encoding="utf-8") as outfile:
            print(get_nome_dos_municipios_do_template_sem_formatar(nome_do_template))
            json_object = json.dumps(get_nome_dos_municipios_do_template_sem_formatar(
                nome_do_template), indent=4, ensure_ascii=False)
            outfile.write(json_object)

    return jsonify('ok')
