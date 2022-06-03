from utils import indexing
from utils import path_functions
from utils import path_functions
from utils.file_to_df import get_df
from utils.check_df import check_all_values_of_column

class ValidadorProcessosLicitatorios:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['receitas'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_numero(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['numero'], typee='valor')
        return isvalid, result

    def predict_modalidade(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['modalidade'], typee='text')
        return isvalid, result
    
    def predict_objeto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['objeto'], typee='text')
        return isvalid, result
    
    def predict_status(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['status'], typee='text')
        return isvalid, result
    
    def predict_resultado(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['resultado'], typee='text')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'numero': {},
            'modalidade': {},
            'objeto': {},
            'status': {},
            'resultado': {},
        }

        # Número
        isvalid, result = self.predict_numero()
        result_explain = self.explain(result, self.keywords['numero'], 'o número')
        resultados['previsao']['predict'] = isvalid
        resultados['previsao']['explain'] = result_explain

        # Modalidade
        isvalid, result = self.predict_modalidade()
        result_explain = self.explain(result, self.keywords['numero'], 'a modalidade')
        resultados['previsao']['predict'] = isvalid
        resultados['previsao']['explain'] = result_explain

        # O objeto
        isvalid, result = self.predict_objeto()
        result_explain = self.explain(result, self.keywords['objeto'], 'o objeto')
        resultados['previsao']['predict'] = isvalid
        resultados['previsao']['explain'] = result_explain

        # Statis
        isvalid, result = self.predict_status()
        result_explain = self.explain(result, self.keywords['status'], 'o status')
        resultados['previsao']['predict'] = isvalid
        resultados['previsao']['explain'] = result_explain

        # Resultado
        isvalid, result = self.predict_resultado()
        result_explain = self.explain(result, self.keywords['resultado'], 'o resultado')
        resultados['previsao']['predict'] = isvalid
        resultados['previsao']['explain'] = result_explain

        return resultados
        
    def explain(self, result, column_name, description):
        try:
            numero_de_entradas = len(result[column_name])
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} da licitação válido: {sum(result['isvalid'])}"""
        return result