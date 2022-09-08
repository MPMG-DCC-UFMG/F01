
import re
from src.validadores.utils import check_df
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.search_html import analyze_html
from src.validadores.utils.check_df import search_in_column
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorRelatorioMensal:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        # print(self.df)

    def predict_relatorio_mensal(self):
        
        files = self.files['html']

        result = analyze_html(files, keyword_to_search=self.keywords['necessary_term'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=len(self.keywords['necessary_term']))

        return isvalid, result
    
    def predict(self):

        resultados = {
            'relatorio_mensal': {},
        }

        # Relatório mensal da despesa com pessoal
        isvalid, result = self.predict_relatorio_mensal()
        result_explain = self.explain(isvalid, self.keywords['explain'])
        resultados['relatorio_mensal']['predict'] = isvalid
        resultados['relatorio_mensal']['explain'] = result_explain

        return resultados
        
    def explain(self, isvalid, description):

        if isvalid:
            return "É " + description
        else:
            return "Não é " + description