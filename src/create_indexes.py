import yaml
# from constant_simplanweb import municipios_simplanweb
from constant_sintese import municipios_sintese
from pathlib import Path
import os
import json
import subprocess
import time

TIME_OUT = 300

# MUNICIPIOS = municipios_simplanweb + municipios_sintese
MUNICIPIOS = municipios_sintese
# MUNICIPIOS = ['ibiai', 'patis', 'veredinha']

# MP
HOME = Path("/home/ufmg.amedeiros")

# Locamente
# HOME = Path.home()

for municipio in MUNICIPIOS:

    config = {
        'name': municipio,
        'fs': 
            {'url': '/datalake/ufmg/crawler/webcrawlerc01/realizacaof01/' + municipio, 
            # {'url': '/home/asafe/GitHub/Coleta_F01/' + municipio, 
            'update_rate': '15m', 
            'excludes': ['*/screenshots*'], 
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
                'enabled': True, 
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
                yaml.dump(config, yaml_file, default_flow_style=False)

    else:
        print("Creating configuration folter:", municipio_directory)
        os.makedirs(municipio_directory)
        print("\tCreating configuration file:", municipio_directory / "_settings.yaml")
        with open(municipio_directory / "_settings.yaml", 'w') as yaml_file:
                yaml.dump(config, yaml_file, default_flow_style=False)


    print('Run crawler')
    process = subprocess.Popen(["/dados01/workspace/ufmg_2021_f01/ufmg.amedeiros/search_engine/fscrawler-es7-2.9/bin/fscrawler", municipio])
    # process = subprocess.Popen(["/home/asafe/Desktop/SearchEngine/fscrawler-es7-2.8-SNAPSHOT/bin/fscrawler", municipio, '--loop 1'])

    try:
        outs, errs = process.communicate(timeout=TIME_OUT)
    except:
        process.kill()
        outs, errs = process.communicate()

    status = municipio_directory / "_status.json"
    if os.path.exists(status):
        f = open(status)
        data = json.load(f)
        print("status:", data)

    print("finish", process.pid, municipio)
