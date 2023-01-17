import os
import yaml
import json
import subprocess
from pathlib import Path
from src.empresa.manage import get_municipios_do_template

TIME_OUT = 600

def scrip_indexar_arquivos_mp(nome_do_template):

    print("Indexando para o template:", nome_do_template)

    MUNICIPIOS = [municipio.nome_formatado for municipio in get_municipios_do_template(nome_do_template)]
    # TODO trocar o usuário

    HOME = Path.home()

    for municipio in MUNICIPIOS:

        # Não abilitado:

        # Descompacta os arquivos .rar (colocar no mesmo diretório, e mantem o .rar original)
        data_lake = Path("/datalake/ufmg/crawler/webcrawlerc01/realizacaof01/")
        diretorio_municipio = data_lake / municipio
        # extrair_arquivos(diretorio_municipio)

        #  -------------

        config = {
            'name': municipio,
            'fs': 
                {'url': '/datalake/ufmg/crawler/webcrawlerc01/realizacaof01/' + municipio, 
                'update_rate': '15m', 
                'excludes': ['*/screenshots*', '*/log*'], 
                'json_support': False, 
                'filename_as_id': False, 
                'add_filesize': True, 
                'remove_deleted': True, 
                'add_as_inner_object': False, 
                'store_source': False, 
                'index_content': True, 
                'attributes_support': False, 
                'raw_metadata': False, 
                'xml_support': False, 
                'index_folders': True, 
                'lang_detect': False, 
                'continue_on_error': False, 
                'ocr': 
                    {'language': 'por', 
                    'enabled': False, 
                    'pdf_strategy': 'auto'}, 
                'follow_symlinks': False},
            'elasticsearch': 
                {'nodes': 
                    [{'url': 'http://127.0.0.1:8055'}], 
                    'bulk_size': 100, 
                    'flush_interval': '5s', 
                    'byte_size': '10mb', 
                    'ssl_verification': True},
        }

        municipio_directory = HOME / ".fscrawler" / municipio
        print(municipio_directory)

        if os.path.exists(municipio_directory):

            if os.path.exists(municipio_directory / "_settings.yaml"):
                with open(municipio_directory / "_settings.yaml") as stream:
                    try:
                        print("Configuration file '" + municipio + "' exist in ", municipio_directory / "_settings.yaml")
                    except yaml.YAMLError as exc:
                        print(exc)

            else:

                print("Creating configuration file:", municipio_directory / "_settings.yaml")
                with open(municipio_directory / "_settings.yaml", 'w') as yaml_file:
                    print("Criando o _settings", municipio)
                    yaml.dump(config, yaml_file, default_flow_style=False)

        else:
            print("Creating configuration folter:", municipio_directory)
            os.makedirs(municipio_directory)
            print("\tCreating configuration file:", municipio_directory / "_settings.yaml")
            with open(municipio_directory / "_settings.yaml", 'w') as yaml_file:
                    yaml.dump(config, yaml_file, default_flow_style=False)


        print('Run crawler')
        process = subprocess.Popen([HOME / "search_engine" / "fscrawler-es7-2.9/bin/fscrawler", municipio, '--loop', '1'])

        try:
            outs, errs = process.communicate(timeout=TIME_OUT)
            print("finish ok", process.pid, municipio)
        except:
            process.kill()
            outs, errs = process.communicate()
            print("finish kill TIME_OUT", process.pid, municipio)

        status = municipio_directory / "_status.json"
        if os.path.exists(status):
            f = open(status)
            data = json.load(f)
            print("status:", data)