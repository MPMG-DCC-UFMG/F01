from ..base import Validador
from src.validadores.utils import indexing
from src.validadores.utils import check_df
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

class ValidadorRegistroDasCompetencias(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        self.job_name = job_name
        if self.keywords['type'] != 'predict_by_number_of_files':
            files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
            files = path_functions.filter_paths(files, words=['competencias'])
            self.files = path_functions.agg_paths_by_type(files)

    def predict_registro_das_competencias(self):
        # Analyze 
        result = analyze_html(self.files['html'], keyword_to_search=self.keywords['keyword_check'])
        #Check result 
        isvalid = check_df.infos_isvalid(result, column_name='matches', threshold=0)
        return isvalid, result

    def explain(isvalid, df):
        if not isvalid:
            result = "Não foi encontrado competências de cada órgão municipal."
        else:
            result = "Quantidade de arquivos analizados: {}. Quantidade de aquivos que possuem competências de cada órgão municipal: {}".format(
                len(df['matches']), sum(df['matches'] > 0))
        return result
    
    def predict(self):

        resultados = {
            'registro_das_competencias': {},
        }

        if self.keywords['type'] == 'predict_by_number_of_files':
            # Prever pela quantida de arquivos
            isvalid, result = self.predict_by_number_of_files(self.job_name, self.keywords['directory'])
            result_explain = self.explain_by_number_of_files(isvalid, result)

        else:
            isvalid, result = self.predict_registro_das_competencias()
            result_explain = self.explain(result)

        resultados['registro_das_competencias']['predict'] = isvalid
        resultados['registro_das_competencias']['explain'] = result_explain

        return resultados
        
