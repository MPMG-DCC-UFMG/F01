import numpy as np
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.file_to_dataframe import get_df

class ValidadorUnidadesAdministrativas:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['unidades_administrativas'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_endereco(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['endereco'], typee='text')
        return isvalid, result
    
    def predict_telefone(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['telefone'], typee='text')
        return isvalid, result
    
    def predict_horario_de_atendimento(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['horario_de_atendimento'], typee='text')
        return isvalid, result
    
    def predict(self):

        resultados = {
            'endereco': {},
            'telefone': {},
            'horario_de_atendimento': {}
        }

        # Endereço
        isvalid, result = self.predict_endereco()
        result_explain = self.explain(result, 'endereço')
        resultados['endereco']['predict'] = isvalid
        resultados['endereco']['explain'] = result_explain

        # Telefone
        isvalid, result = self.predict_telefone()
        result_explain = self.explain(result, 'telefone')
        resultados['telefone']['predict'] = isvalid
        resultados['telefone']['explain'] = result_explain

        # Horario de atendimento
        isvalid, result = self.predict_horario_de_atendimento()
        result_explain = self.explain(result, 'horário de atendimento')
        resultados['horario_de_atendimento']['predict'] = isvalid
        resultados['horario_de_atendimento']['explain'] = result_explain

        return resultados
        
    def explain(self, result, description):
        result = f"""O {description} de alguma Unidade Administrativa é válido."""
        return result