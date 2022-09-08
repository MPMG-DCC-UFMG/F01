import os
import subprocess
# import patoolib
from pathlib import Path
import zipfile 
import rarfile

from src.validadores.utils.path_functions import list_files

def extrair_arquivos(diretorio, path_to_file=None):
    """
    Descrição: Extrai todos os arquivos compactados em de diretório (rar ou zip).

    Parameters
    ----------
    diretorio: pathlib.PosixPath 
        Diretório que sera analisado
    path_to_file: pathlib.PosixPath 
        Diretório que os arquivos extraidos serão salvos. Opcional, caso nulo será o mesmo analisado.

    Returns
    -------
    none
    """

    extensoes = ["pdf", "csv", "xls", "html", 
            "pdf", "doc", "bat", "rar", "zip", "tar"
            "png", "json", "out", "err", "jsonl"]

    paths = list_files(diretorio)
    
    for path in paths: 
        # Salva no diretório atual se nenhum caminho for passado
        if not path_to_file:
            path_to_file = os.sep.join(path.split(os.sep)[:-1])

        split_path = path.split('.')

        # Vê se tem extensão
        if (split_path[-1] in extensoes):
            type_ = split_path[-1]
        else:
            # Caso não tenha uma das extensões acima, detecta o tipo
            type_ = subprocess.check_output(["file", path], text=True)
            if ("RAR archive data" in type_):
                type_ = 'rar'
            if ("Zip archive data" in type_):
                type_ = 'zip'

        if ("rar" in type_):
            rarfile.RarFile(path).extractall(path_to_file)
        
        elif zipfile.is_zipfile(path):
            zipfile.ZipFile(path).extractall(path_to_file)
        


def compactar_arquivos(diretorio, path_to_file, tipo_de_compactacao=None):
    """
    Descrição: Compacta arquivos de um diretório em rar ou zip.

    Parameters
    ----------
    diretorio: pathlib.PosixPath 
        Diretório que sera analisado
    path_to_file: pathlib.PosixPath 
        Diretório que será salvo o arquivo compactado. Opcional, caso nulo será o mesmo.

    Returns
    -------
    none
    """

    if not tipo_de_compactacao:
        tipo_de_compactacao = 'zip'

    paths = list_files(diretorio)

    # ZIP
    if tipo_de_compactacao== 'zip':

        z = zipfile.ZipFile(path_to_file, 'w', zipfile.ZIP_DEFLATED)
        for file_path in paths:

            z.write(file_path)
        z.close()

    # TO DO
    # RAR
    elif tipo_de_compactacao== 'rar':

        # patoolib.create_archive(path_to_file, paths)

        pass    