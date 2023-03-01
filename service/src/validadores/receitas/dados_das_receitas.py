from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column
class ValidadorDadosDasReceitas:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['receitas'])
        self.files = path_functions.agg_paths_by_type(files)
        try:
            max_files = keywords['max_files']
        except KeyError:
            max_files = 5

        print(len(self.files['html']))
        self.df = get_df(self.files, keywords['types'], max_files=max_files)
        self.df.to_csv('aux.csv')

    # Previsão
    def predict_previsao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['previsao'], typee='valor')
        return isvalid, result

    # Arrecadação
    def predict_arrecadacao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['arrecadacao'], typee='valor')
        return isvalid, result
    
    # Classificação
    def predict_classificacao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['classificacao'], typee='text')
        return isvalid, result
    

    def predict(self):

        resultados_dados_das_receitas = {
            'previsao': {},
            'arrecadacao': {},
            'classificacao': {},
        }

        # Preivsão
        isvalid, result = self.predict_previsao()
        result_explain = self.explain(result, self.keywords['previsao'], 'a previsão')
        resultados_dados_das_receitas['previsao']['predict'] = isvalid
        resultados_dados_das_receitas['previsao']['explain'] = result_explain

        # Arrecadação
        isvalid, result = self.predict_arrecadacao()
        result_explain = self.explain(result, self.keywords['arrecadacao'], 'a arrecadação')
        resultados_dados_das_receitas['arrecadacao']['predict'] = isvalid
        resultados_dados_das_receitas['arrecadacao']['explain'] = result_explain

        # Classificação
        isvalid, result = self.predict_classificacao()
        result_explain = self.explain(result, self.keywords['classificacao'], 'a classificação')
        resultados_dados_das_receitas['classificacao']['predict'] = isvalid
        resultados_dados_das_receitas['classificacao']['explain'] = result_explain

        return resultados_dados_das_receitas
        
    def explain(self, result, column_name, description):
        result = f"""Quantidade de entradas que possuem o campo {description} da receita válido: {sum(result['isvalid'])}"""
        return result