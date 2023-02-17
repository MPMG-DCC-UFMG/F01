from bs4 import BeautifulSoup
import re
import pandas as pd
import codecs
import tabula
import random
from functools import reduce
from src.validadores.utils import read
from src.validadores.utils.detect_delimiter import detect_delimiter

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
    Não faz isso para o que já está dentro de uma tag table
    
    Parameters
    ----------
    soup: bs4.BeautifulSoup
        Html a ser convertido
        
    Returns
    -------
    Dataframe
        Um df.
    """

    body = soup.body #Ele começa acessando o elemento <body> do documento usando soup.body.
    body.script.clear() #Removendo as tags <scrip>
    # try:
    #     body.table.clear()  #Pular elementos que estão dentro de uma tabela
    # except AttributeError:
    #     pass

    df_= {}

    for element in body.next_elements:
        #O atributo next_elements retorna um iterador que retorna recursivamente 
        # todos os descendentes do elemento e seus próximos irmãos, na ordem do documento.
        textos_da_tag = [text for text in element.stripped_strings]   
        for texto in textos_da_tag:
            if ":" in repr(texto):
                key_value = element.getText().strip() #Extrair o texto limpo de cada elemento chamando o atributo 
                # stripped_strings. Isso retorna um iterador sobre todas as strings de texto no elemento,
                # sem espaços em branco no início e no final.
                key_value = re.split(';|:|\n', key_value)
                if (len(key_value) == 2):
                    key = key_value[0]
                    value = key_value[1]
                    if value != '':
                        df_[key] = value


    # Caso estejam em tags diferentes
    # Exemplo:
    """
    <b>Endereço: </b>
    Praça Moisés Ladeia 
    <br>
    """
    next_is_value = 0
    key = ''
    for element in body.next_elements:
        textos_da_tag = [text for text in element.stripped_strings] 
        if len(textos_da_tag) == 1:
            if textos_da_tag[0][-1] == ':':
                key = textos_da_tag[0].replace(":","")
                next_is_value = 1
                continue

            if next_is_value == 1:
                next_is_value = 0
                value = textos_da_tag[0]
                df_[key] = value

    df = pd.DataFrame(df_,index=[0])

    return df


def convert_html(soup):
    """
    Converte todas as tabelas de um hmtl em um Dataframe, 
    Além das tags 'table' também transforma as informações separadas 
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
            # print(file_name)
            soup = read.read_html(file_name)
            new_df = convert_html(soup)
            new_df['FileName'] = file_name
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
        for i in paths:

            delimiter = detect_delimiter(i)
            if not delimiter:
                print("WARNING: delimiter not found for", i)
                continue
            tabela = pd.read_csv(i, delimiter=delimiter, on_bad_lines='skip')
            
            aux = 0

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
            if not "2eb21eca-8cc1-4655-aae9-23c6b64e3daa.pdf" in i:
                continue

            if number_pdf == 10:
                break
            # print(number_pdf, i)
            try:
                lista_tabelas = tabula.read_pdf(i, pages='all')
                if len(lista_tabelas) > 0:
                    number_pdf += 1
                    
                for tabela in lista_tabelas:
                    # print(type(tabela))
                    tabela.to_csv("tmpe.csv")
                    # print(tabela)

                    if ('Unnamed' in ' '.join(tabela.columns.values)):
                        tabela.columns = tabela.loc[0].values
                        tabela.drop(0 , inplace=True)

                        tabela = tabela.loc[:number_entry_each_table]

                    list_dfs.append(tabela)
                    break
            except:
                print(f"Falha em converter o pdf :{i} em dataframe")
                continue
                
    
        df = concat_lists(list_dfs)

    else:
        df = pd.DataFrame()

    df = df.drop_duplicates()
    return df

def get_df(files, ttype, max_files=None):
    """
    Converte uma lista de arquivos de um tipo em uma tabela (dataframe)
    """
    df_final = pd.DataFrame()
    for key, values in files.items():
        if not key in ttype: # Converte apenas o arquivos com um tipo em 'ttype'
            continue
        if max_files: # Pode limitar  a quantidade
            # random;seed(0) # ativar quando estiver depurando o problema
            # values = random.sample(values, max_files)
            values = values[:max_files]
        print(values)
        df = load_and_convert_files(paths=values, format_type=key)
        df_final = pd.concat([df, df_final], axis=0, ignore_index=True)
        df_final = df_final.drop_duplicates()
    return df_final

def html_to_df(files, max_files=None):
    if max_files:
        files = files[:max_files]

    # abre os arquivos e transforma-os em um objeto Beatifulsoup
    files = list(map(lambda x: BeautifulSoup(open(x, 'r'), 'html.parser'), files))
    # encontra todas as tabelas de cada arquivo com uma determinada classe
    files = list(map(lambda x: x.find_all('table', class_="ContasPublicas"), files))
    # transforma as listas de tabelas de cada arquivo em uma única lista
    tables = reduce(lambda x,y: x+y, files)
    # função que encontra elementos html com o texto exigido
    find_objetos = lambda x: x.find(lambda tag: tag.name == 'td' and 'Objeto:' in tag.text)
    # executa a função de encontrar os elementos em todas as tablelas
    objetos = list(map(lambda x: find_objetos(x), tables))
    # extrai o texto das tabelas
    objetos = list(map(lambda x: x.text if x else None, objetos))
    # remove informações não relevantes do texto extraído
    objetos = list(map(lambda x: x.replace('Objeto: ', '') if x else None, objetos))
    print(len(objetos))
    # retorna quantas entradas válidas existem depois da remoção
    isvalid = list(map(lambda x: x is not None and x is not '', objetos))
    print(sum(isvalid))

    test_html = """<td align="Left">Número do Processo Licitatório: <a href="javascript:exibirDadosLicitacao(&quot;00032017&quot;, &quot;B&quot;, &quot;1&quot;)">00032017</a></td>"""

    html = BeautifulSoup(test_html, 'html.parser')

    print(html.text)

    return None

    