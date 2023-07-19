from flask import jsonify
from flask import Blueprint
from pathlib import Path

from src.municipio.manage import get_municipio
from src.api_de_integracao.manage import salvar_resultado_de_json
from src.empresa.manage import get_nome_dos_municipios_do_template
from src.validadores.utils.handle_files import get_keywords_do_template

validadores = Blueprint('validadores', __name__)

from src.validadores import pipeline_validadores

@validadores.route('/')
def index():
    print('validadores')
    return jsonify('Validadores.')


@validadores.route('/<string:nome_do_template>', methods=['GET'])
def rodar_template(nome_do_template):
    """Executar validadores - (Em desenvolvimento)
    Este endpoint executa os todos validadores desenvolvidos para todos os municípios de um template, 
    salvando o resultado no banco de dados.
    ---
    tags:
      - Execução dos validadores
    parameters:
      - name: nome_do_template
        in: path
        type: string
        required: true
        description: Nome do template para validação
      - name: nome_da_tag
        in: path
        type: string
        required: true
        description: Nome do tag para validação
    responses:
      200:
        description: Sucesso na va dos arquivos
        schema:
          type: string
          example: 'ok'
    """

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
    """Executar validadores - (Em desenvolvimento)
    Este endpoint executa os validadores de uma tag específica para todos os municípios de um template, 
    salvando o resultado no banco de dados.
    ---
    tags:
      - Execução dos validadores
    parameters:
      - name: nome_do_template
        in: path
        type: string
        required: true
        description: Nome do template para validação
    responses:
      200:
        description: Sucesso na va dos arquivos
        schema:
          type: string
          example: 'ok'
    """

    parametros = get_keywords_do_template(nome_do_template)
    municipios = get_nome_dos_municipios_do_template(nome_do_template)
    print(municipios)
    for municipio in municipios:
            print('-rodando município:', municipio)
            if nome_da_tag == 'acesso_a_informacao':
                resultado = pipeline_validadores.acesso_a_informacao(parametros, municipio)
            elif nome_da_tag == 'contratos':
                resultado = pipeline_validadores.contratos(parametros, municipio)
            elif nome_da_tag == 'terceiro_setor':
                resultado = pipeline_validadores.terceiro_setor(parametros, municipio)
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
            elif nome_da_tag == 'orcamento':
                resultado = pipeline_validadores.orcamento(parametros, municipio)
            else:
                return jsonify(f"Tag {nome_da_tag} não existe")
            
            print(f"resultado final: {municipio}")
            municipio = get_municipio(municipio)
            print(resultado)
            print("**********************")
        
            salvar_resultado_de_json(municipio_id=municipio.id, resultado_json=resultado)
            

    return jsonify(f"Template {nome_do_template} validado") 


# Para testes
@validadores.route('/find/<string:nome_do_template>/<string:nome_da_tag>/<string:nome_da_subtag>', methods=['GET'])
def encontar_arquivos_sug_tag(nome_do_template, nome_da_tag, nome_da_subtag):

    nome_da_subtag
    nome_do_template
    municipios = get_nome_dos_municipios_do_template(nome_do_template)
    for municipio in municipios:

        job_diretory = Path("/datalake","ufmg","crawler","webcrawlerc01","realizacaof01", municipio)

        # raw_pages
        full_path = job_diretory / nome_da_tag / nome_da_subtag / "data" / "raw_pages"

        if not full_path.exists():
            print("Directory does not exist.")

        raw_pages = full_path.glob('*')
        number_of_raw_pages = len(list(raw_pages)) - 1 # Descartando o file_description.jsonl

        # files html
        full_path = job_diretory / nome_da_tag / nome_da_subtag / "data" / "files"

        if not full_path.exists():
            print("Directory does not exist.")

        files = full_path.glob('*')
        number_of_files = len(list(files)) - 1  # Descartando o file_description.jsonl
        isvalid = (number_of_files > 0) or (number_of_raw_pages > 0)
        print(municipio)
        print("number_of_files:", number_of_files, "number_of_raw_pages", number_of_raw_pages )
        print()

    print(isvalid)
    return jsonify(f"{nome_do_template, nome_da_tag, nome_da_subtag}") 