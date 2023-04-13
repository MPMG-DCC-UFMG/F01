
import re
from src.validadores.utils import check_df
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

class ValidadorRelatorioMensal:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)

    def predict_relatorio_mensal(self):
        
        files = self.files['html']

        result = analyze_html(files, keyword_to_search=self.keywords['necessary_term'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=len(self.keywords['necessary_term']))

        return isvalid, result
    
    def predict(self):

        resultados = {
            'relatorios_despesas_com_pessoal': {},
        }

        # Relatório mensal da despesa com pessoal
        isvalid, _ = self.predict_relatorio_mensal()
        result_explain = self.explain(isvalid, self.keywords['explain'])
        resultados['relatorios_despesas_com_pessoal']['predict'] = isvalid
        resultados['relatorios_despesas_com_pessoal']['explain'] = result_explain

        return resultados
        
    def explain(self, isvalid, description):

        if isvalid:
            return "É " + description
        else:
            return "Não é " + description