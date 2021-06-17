import pandas as pd


def format_values(df, column_name):
    
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].str.replace("R\$", '')
    df[column_name] = df[column_name].str.replace(".", '')
    df[column_name] = df[column_name].str.replace(",", '.')
    df[column_name] = df[column_name].astype(float)
    
    return df
