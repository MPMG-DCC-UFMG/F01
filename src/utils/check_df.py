def contains_keyword(df, word):
    """
    Verifica se um dataframe possui uma coluna cujo nome contém uma palavra-chave especifica
    """

    columns = [i.lower() for i in df.columns]
    i = 0
    for column_name in columns:

        finder = column_name.find(word)
        if finder != -1:
            return True, df.columns[i]
    
        i +=1
        
    return False, word

def infos_isvalid(df, column_name, threshold=0): 
    """
    Verifica se a quantidade de informações válidas no dataframe é maior que um valor de threshold.
    """
    
    if sum(df[column_name]) > threshold:
        return True
    else:
        return False

def files_isvalid(df, column_name, threshold=0): 
    """
    Verifica se a quantidade de arquivos válidos em um arquivo é maior que um valor de threshold.
    """
    
    for i in df[column_name]:
        if i > threshold:
            return True
    return False

    