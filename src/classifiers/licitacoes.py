from bs4 import BeautifulSoup
import re
import os
import sys
import pandas as pd
#sys.path.insert(0, '/home/cinthia/F01/src')

sys.path.insert(0, '../')

from utils import indexing
from utils import html_to_csv
from utils import path_functions
from utils import check_df
from utils import read

def analyze_inexibilidade (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é inexibilidade
    """
    try:
        if re.search("inexigibilidade", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False
    except TypeError:
        return False

def analyze_dispensa (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é dispensa
    """
    try:
        if re.search("dispensa", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False
    except TypeError:
        return False

def analyze_resultado (df, column_name):
    """
    Verifica se na coluna resultado há algum arquivo com nome associado a resultado
    """
    if len(df[column_name].value_counts()) > 1:
        return True
    else:
        return False

def analyze_busca(format_path):
    """
    Verifica se os documentos html possuem o campo "Filtrar Pesquisa"
    """

    try:
        soup = read.read_html(format_path)
        text = soup.get_text()

        if re.search("filtrar\s*pesquisa|filtrar|pesquisar", text, re.IGNORECASE) != None:
            return True
    
    except TypeError or UnicodeDecodeError:
        return False
        
    return False

def analyze_edital(df, column_name):
    """
    Verifica se na coluna Editais há algum arquivo
    """
    if len(df[column_name].value_counts()) > 1:
        return True
    else:
        return False

def check_all_files_busca(paths, result):

    for file_name in paths:
        result['busca'].append(analyze_busca(file_name))

    return result

def get_df(files, ttype):
    df_final = pd.DataFrame()
    for key, values in files.items():
        if key in ttype:
            df = html_to_csv.load_and_convert_files(paths=values, format_type=key)
            df_final = pd.concat([df, df_final], axis=0, ignore_index=True)
    return df_final

class Licitacoes:

    def __init__(self, files, keywords_check, ttype):
        self.files = files
        self.keywords_check = keywords_check
        self.df = get_df(self.files, ttype)

    def analyze_procedimentos_licitatorios(self, df, keyword): 
        """
        Verifica se existe um coluna com a palavra-chave e se cada valor nela é nulo ou não
        """
        val = { keyword: []}
        if df is not None:
            isvalid, column_name = check_df.contains_keyword(df=df, word=keyword)
            if isvalid:
                val[keyword] = list(~df[column_name].isna())
                return val
        val[keyword] = []
        return val

    def predict_df(self, keyword_check):
        result = self.analyze_procedimentos_licitatorios(self.df, keyword_check)
        isvalid = check_df.infos_isvalid(result, keyword_check, threshold=0)
        return isvalid, result

    def predict_inexibilidade(self):

        result = {'inexigibilidade': []}

        if self.df is None:
            return False, result

        if "Número Modalidade" in self.df.columns:
            self.df.drop(columns=["Número Modalidade"],inplace=True)

        #Analyze
        isvalid, column_modalidade = check_df.contains_keyword(self.df, word='modalidade')

        for index, value in self.df.iterrows():
            result['inexigibilidade'].append(analyze_inexibilidade (value, column_modalidade))

        #Check
        isvalid = check_df.infos_isvalid(result, column_name='inexigibilidade', threshold=0)
            
        return isvalid, result

    def predict_dispensa(self):
        result = {'dispensa': []}

        if self.df is None:
            return False, result

        if "Número Modalidade" in self.df.columns:
            self.df.drop(columns=["Número Modalidade"],inplace=True)

        #Analyze
        isvalid, column_modalidade = check_df.contains_keyword(self.df, word='modalidade')

        for index, value in self.df.iterrows():
            result['dispensa'].append(analyze_dispensa (value, column_modalidade))

        #Check
        isvalid = check_df.infos_isvalid(result, column_name='dispensa', threshold=0)
        return isvalid, result


    def predict_resultado(self, keyword_check): 
        result = {'resultado': []}
        #Analyze
        isvalid, column_modalidade = check_df.contains_keyword(self.df, word=keyword_check)

        if isvalid:
            result['resultado'].append(analyze_resultado (self.df, column_modalidade))
                
        #Check
        isvalid = check_df.infos_isvalid(result, column_name='resultado', threshold=0)
        return isvalid, result


    def predict_editais(self, keyword_check):
        result = {'editais': []}
        #Analyze
        isvalid, column_edital = check_df.contains_keyword(self.df, word=keyword_check)
        if isvalid:
            result['editais'].append(analyze_edital(self.df, column_edital))

        # print(self.df['Editais de Licitação e Demais Arquivos'])
        #Check
        isvalid = check_df.infos_isvalid(result, column_name='editais', threshold=0)
        return isvalid, result

    def predict_busca(self): 

        html_files = self.files['html']
        result = {'busca': []}

        #Analyze
        result = check_all_files_busca(html_files, result)

        #Check
        isvalid = check_df.infos_isvalid(result, column_name='busca', threshold=0)
        
        return isvalid, result

def explain(df, column_name):

    result = "Explain - Quantidade de entradas analizadas: {}\n\tQuantidade de entradas válidas: {}\n".format(
         len(df[column_name]), sum(df[column_name]))

    return result