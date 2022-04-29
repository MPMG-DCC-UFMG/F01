from utils import html_to_csv
import pandas as pd


def get_df(files, ttype):
    df_final = pd.DataFrame()
    for key, values in files.items():
        if key in ttype:
            df = html_to_csv.load_and_convert_files(paths=values, format_type=key)
            df_final = pd.concat([df, df_final], axis=0, ignore_index=True)
    return df_final