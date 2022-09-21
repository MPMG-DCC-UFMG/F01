from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorProcessosLicitatorios:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['licitacao'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        print(self.df.columns)
        print(self.df)

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
        resultados['numero']['predict'] = isvalid
        resultados['numero']['explain'] = result_explain

        # Modalidade
        isvalid, result = self.predict_modalidade()
        result_explain = self.explain(result, self.keywords['modalidade'], 'a modalidade')
        resultados['modalidade']['predict'] = isvalid
        resultados['modalidade']['explain'] = result_explain

        # O objeto
        isvalid, result = self.predict_objeto()
        result_explain = self.explain(result, self.keywords['objeto'], 'o objeto')
        resultados['objeto']['predict'] = isvalid
        resultados['objeto']['explain'] = result_explain

        # Status
        isvalid, result = self.predict_status()
        result_explain = self.explain(result, self.keywords['status'], 'o status')
        resultados['status']['predict'] = isvalid
        resultados['status']['explain'] = result_explain

        # Resultado
        isvalid, result = self.predict_resultado()
        result_explain = self.explain(result, self.keywords['resultado'], 'o resultado')
        resultados['resultado']['predict'] = isvalid
        resultados['resultado']['explain'] = result_explain

        return resultados
        
    def explain(self, result, column_name, description):
        try:
            numero_de_entradas = len(result[column_name])
        except KeyError:
            numero_de_entradas = 0

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem o campo {description} da licitação válido: {sum(result['isvalid'])}"""
        return result