from flask import jsonify
from flask import Blueprint
import pprint


from src.municipio.manage_municipios import get_municipio
from src.api_de_integracao.manage import salvar_resultado_de_json
from src.empresa.manage import get_nome_dos_municipios_do_template
from src.validadores.utils.handle_files import get_keywords_do_template

validadores = Blueprint('validadores', __name__)

from src.validadores import pipeline_validadores

@validadores.route('/')
def index():
    print('validadores')
    return jsonify('Validadores.')


@validadores.route('/<string:nome_do_template>', methods=['POST', 'GET'])
def rodar_template(nome_do_template):

    parametros = get_keywords_do_template(nome_do_template)
    municipios = get_nome_dos_municipios_do_template(nome_do_template)
    
    for municipio in municipios:

        print(municipio)
        resultado = pipeline_validadores.todas_tags(parametros, municipio)

        municipio = get_municipio(municipio)
        print("resultado final")
        print(resultado)

        # print("Salvando resultado")
        salvar_resultado_de_json(municipio_id=municipio.id, resultado_json=resultado)

    return jsonify(f"Template {nome_do_template} validado") 

@validadores.route('/<string:nome_do_template>/<string:nome_da_tag>', methods=['GET'])
def rodar_tag(nome_do_template, nome_da_tag):

    parametros = get_keywords_do_template(nome_do_template)
    municipios = get_nome_dos_municipios_do_template(nome_do_template)
    
    for municipio in municipios:
        # if municipio == 'brumadinho':
            print('-rodando município:', municipio)

            if nome_da_tag == 'acesso_a_informacao':
                resultado = pipeline_validadores.acesso_a_informacao(parametros, municipio)
            elif nome_da_tag == 'contratos':
                resultado = pipeline_validadores.contratos(parametros, municipio)
            elif nome_da_tag == 'concursos_publicos':
                resultado = pipeline_validadores.concursos_publicos(parametros, municipio)
            elif nome_da_tag == 'servidores_publicos':
                resultado = pipeline_validadores.servidores_publicos(parametros, municipio)
            elif nome_da_tag == 'receitas':
                resultado = pipeline_validadores.receitas(parametros, municipio)
            elif nome_da_tag == 'despesas':
                resultado = pipeline_validadores.despesas(parametros, municipio)
            elif nome_da_tag == 'obras_publicas':
                resultado = pipeline_validadores.obras_publicas(parametros, municipio)
            elif nome_da_tag == 'despesas_com_diarias':
                resultado = pipeline_validadores.despesas_com_diarias(parametros, municipio)
            elif nome_da_tag == 'informacoes_institucionais':
                resultado = pipeline_validadores.informacoes_institucionais(parametros, municipio)
            elif nome_da_tag == 'licitacoes':
                resultado = pipeline_validadores.licitacoes(parametros, municipio)
            else:
                return jsonify(f"Tag {nome_da_tag} não existe")
            
            print(f"resultado final: {municipio}")
            municipio = get_municipio(municipio)
            print(resultado)
            # pprint.pprint(resultado, indent=2)
            print("**********************")
        

<<<<<<< HEAD
            # salvar_resultado_de_json(municipio_id=municipio.id, resultado_json=resultado)
=======
        #salvar_resultado_de_json(municipio_id=municipio.id, resultado_json=resultado)
>>>>>>> pt_contratos_dados_dos_contratos

    return jsonify(f"Template {nome_do_template} validado") 
