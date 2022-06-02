from bs4 import BeautifulSoup
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


def convert_html(soup):
    """
    Converte todas as tabelas de um html em um df, concatenando lista de df em um único df.
         
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Html a ser convertido
        
    Returns
    -------
    Dataframe
        Um único df concatenado.
    """

    try:
        list_dfs = [pd.read_html(str(table))[0] for table in soup.find_all('table')]
        df = concat_lists(list_dfs)
    except ValueError:  
        df = list_to_text(soup)

    return df

def one_html_to_csv (format_path):
    """
    Convert um elemento do html para um dataframe.
    """
    try: 

        soup = read.read_html(format_path)
        df = convert_html(soup)
        return df
        
    except ValueError:
        pass

    return pd.DataFrame()

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

    if format_type == 'html':
        list_df = []
        for file_name in paths:
            new_df = one_html_to_csv(file_name)
            if(not new_df.empty):
                list_df.append(new_df)
        if len(list_df) == 0:
            df = pd.DataFrame()
        else:
            df = pd.concat(list_df)

    elif format_type == 'csv':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(i))

        df = concat_lists(list_csv)
    
    elif format_type == 'bat':

        list_csv = []
        for i in  paths:
            tabela = pd.read_csv(i)
            
            aux = 0

            #  Para Template GRP, que começava com um cabeçalho de colunas  
            while(type(tabela.columns[0]) is not str):
                tabela.columns = tabela.iloc[aux].values
                aux += 1

            list_csv.append(tabela)
        df = concat_lists(list_csv)
    
    elif format_type == 'doc':

        list_csv = []
        for i in  paths:
            list_csv.append(pd.read_csv(i))
        df = concat_lists(list_csv)

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
    
    df = df.drop_duplicates()
    return df
