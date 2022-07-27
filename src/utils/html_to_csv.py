from bs4 import BeautifulSoup
import bs4
import re
import pandas as pd
import codecs
import tabula
from utils import read

def read_content(path, folder, file):
    try:
        file = codecs.open("{}/{}/{}".format(path, folder, file), 'r', 'utf-8')
        soup = BeautifulSoup(file, features="lxml")
    except:
        file = codecs.open("{}/{}/{}".format(path, folder, file), 'r', 'latin-1')
        soup = BeautifulSoup(file, features="lxml")
    
    return soup

def list_to_text(soup):

    type = []
    text = []
    try:
        for i in soup.find("div", { "id" : "detalhes" }).findAll('li'):
            info = i.get_text().split(": ")
            if len(info) >= 2:
                type.append(info[0].lower().replace("\n", ''))
                text.append(''.join(info[1:]))
            elif len(info) == 1:
                type.append(info[0].lower().replace("\n", ''))
                text.append("")
        df = pd.DataFrame([text], columns=type)

    except AttributeError:
        df = pd.DataFrame()
        pass

    return df

def informacao_dois_pontos_para_df(soup):
    """
    Converte as informações separadas por dois pontos de um html em um Dataframe.
         
    Parameters
    ----------
    soup: bs4.BeautifulSoup
        Html a ser convertido
        
    Returns
    -------
    Dataframe
        Um df.
    """

    body = soup.body
    body.script.clear()

    df_= {}

    for element in body.next_elements:

            textos_da_tag = [text for text in element.stripped_strings]    
            for texto in textos_da_tag:
                if ":" in repr(texto):
                    key_value = element.getText().strip()
                    key_value = re.split(';|:|\n', key_value)
                    # print(key_value)
                    if (len(key_value) == 2):
                        key = key_value[0]
                        value = key_value[1]
                        if value != '':
                            df_[key] = value


    df = pd.DataFrame(df_,index=[0])

    return df


def convert_html(soup):
    """
    Converte todas as tabelas de um hmtl em um Dataframe, 
    Além das tags 'table' também transforma as informaçõs separadas 
    por dois pontos, exemplo: Em "Número do contrato: 412" uma coluna
    no dataframe será "Número do contrato", e com uma entrada, "412"
         
    Parameters
    ----------
    soup: bs4.BeautifulSoup
        Html a ser convertido
        
    Returns
    -------
    Dataframe
        Um único dataframe.
    """


    list_dfs = []
    for table in soup.find_all('table'):
        try:
            list_dfs.append(pd.read_html(str(table))[0])
        except ValueError:
            print("Erro ao converter tabela")
            pass
    # list_dfs = [pd.read_html(str(table))[0] for table in soup.find_all('table')]

    df_from_li = list_to_text(soup)
    if (not df_from_li.empty):
        list_dfs.append(df_from_li)

    df_dois_pontos = informacao_dois_pontos_para_df(soup)
    if (not df_dois_pontos.empty):
        list_dfs.append(df_dois_pontos)

    df = concat_lists(list_dfs)

    return df

def one_html_to_csv (format_path):
    """
    Convert um elemento do html para um dataframe.
    """

    soup = read.read_html(format_path)
    df = convert_html(soup)
    return df

# def all_lists_to_csv(paths):

#     list_df = []
#     for file_name in paths:
#         print(file_name)
#         new_df = one_html_to_csv(file_name)
#         if(not new_df.empty):
#             list_df.append(new_df)
#     if (len(list_df)):              
#         return pd.concat(list_df)
#     else: 
#         return pd.DataFrame()

def concat_lists(files):
    """
    Concatena uma lista de df em um único df
         
    Parameters
    ----------
    files : list
        Dataframes a serem concatenados
        
    Returns
    -------
    Dataframe
        Um único df concatenado.
    """
    if len(files) == 0:
        df = pd.DataFrame()
    elif len(files) == 1:
        df = files[0]
    else:
        df = pd.concat(files)
    return df

def load_and_convert_files(paths, format_type):
    """
    Converte uma lista de arquivos de um tipo em uma tabela (dataframe)
         
    Parameters
    ----------
    paths : list of strings
        Lista de arquivos a serem convertidos em uma tabela
        
    Returns
    -------
    Dataframe
        Um único df com todas as tabela desses arquivos.
    """


    if format_type == 'html':
        list_to_concat = []
        df = pd.DataFrame()
        for file_name in paths:
            new_df = one_html_to_csv(file_name)
            list_to_concat.append(new_df)
        if len(list_to_concat) != 0:
            df = pd.concat(list_to_concat)

    elif format_type == 'csv':

        list_to_concat = []
        for i in  paths:
            list_to_concat.append(pd.read_csv(i))

        df = concat_lists(list_to_concat)
    
    elif format_type == 'bat':

        list_to_concat = []
        for i in  paths:
            tabela = pd.read_csv(i)
            
            aux = 0

            #  Para Template GRP, que começava com um cabeçalho de colunas  
            while(type(tabela.columns[0]) is not str):
                tabela.columns = tabela.iloc[aux].values
                aux += 1

            list_to_concat.append(tabela)
        df = concat_lists(list_to_concat)
    
    elif format_type == 'doc':

        list_to_concat = []
        for i in  paths:
            list_to_concat.append(pd.read_csv(i))
        df = concat_lists(list_to_concat)

    elif format_type == 'xls':

        list_xls = []
        for i in  paths:
            list_xls.append(pd.read_excel(i))

        df = concat_lists(list_xls)

    elif format_type == 'pdf':

        number_entry_each_table = 1
        number_of_tables_per_doc = 1

        list_dfs = []
        number_pdf = 0
        for i in paths:

            if number_pdf == 10:
                break
            # print(number_pdf, i)
            lista_tabelas = tabula.read_pdf(i, pages='all')
            if len(lista_tabelas) > 0:
                number_pdf += 1
                
            for tabela in lista_tabelas:
                # print(tabela)
                if ('Unnamed' in ' '.join(tabela.columns.values)):
                    tabela.columns = tabela.loc[0].values
                    tabela.drop(0 , inplace=True)

                    tabela = tabela.loc[:number_entry_each_table]

                list_dfs.append(tabela)

                break
                
    
        df = concat_lists(list_dfs)

    else:
        df = pd.DataFrame()

    df = df.drop_duplicates()
    return df
