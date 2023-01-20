import csv
from collections import Counter

delimiters = [';', ',']
N_LINES = 10

def detect_delimiter(file_path, n_lines=N_LINES):
    """
    Detectar o delimitador de um arquivo csv dentre [';', ',']
    
     Parâmetros:
         - file_path : str : caminho do arquivo a ser lido
         - n_lines : int : número de linhas a serem lidas para detectar o delimitador, opcional, o padrão é 10
        
     Retorna:
         - str : delimitador se encontrado, nenhum caso contrário
    """
    with open(file_path, 'r') as f:
        lines = [next(f) for x in range(n_lines)]
        delimiter_count = Counter()
        for delimiter in delimiters:
            for line in lines:
                delimiter_count[delimiter] += len(line.split(delimiter))
        return delimiter_count.most_common(1)[0][0]

