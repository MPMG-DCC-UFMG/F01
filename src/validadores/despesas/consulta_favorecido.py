from utils import indexing
from utils import check_df
from ..base import Validador
from utils import path_functions
from utils.csv_to_df import get_df
from utils.search_html import analyze_html

class ValidadorConsultaFavorecido(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['pagamentos', 'empenhos'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files

    # Possibilita a consulta de empenhos ou pagamentos por favorecido	
    def predict_favorecido(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)

        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result

    def predict(self):

        resultados_consulta_favorecido = {
            'consulta_favorecido': {},
        }

        isvalid, result = self.predict_favorecido(self.keywords['keyword_check'])
        result_explain = self.explain(result, self.keywords['keyword_check'])
        resultados_consulta_favorecido['consulta_favorecido']['predict'] = isvalid
        resultados_consulta_favorecido['consulta_favorecido']['explain'] = result_explain

        return resultados_consulta_favorecido
        
    def explain(self, result, keywords):
        
        if len(keywords) > 1:
            result = "Os palavras chaves {} estão presentes {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords, sum(result['matches']))
        else:
            result = "A palavra chave '{}' está presente {} vezes em páginas de empenhos ou pagamentos ".format(
                keywords[0], sum(result['matches']))

        return result