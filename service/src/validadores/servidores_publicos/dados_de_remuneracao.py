
from src.validadores.utils import check_df
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html
from src.validadores.utils.file_to_dataframe import get_df, html_to_df
from src.validadores.utils.check_df import search_in_column

class ValidadorDadosDeRemuneracao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        try:
            self.df = html_to_df(self.files['html'], keywords['html_to_df'],keywords['max_files'])
        except KeyError:
            self.df = get_df(self.files, keywords['types'])
        # self.df.to_csv('aux.csv')

    def predict_agentes_politicos(self):

        keywords = ["prefeito", "vereador", "secretário"]
        result = search_in_column(self.df, self.keywords['agentes_politicos'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result

    def predict_servidores_efetivos(self):

        keywords = ["EFETIVO","Efetivo"]
        result = search_in_column(self.df, self.keywords['servidores_efetivos'], keywords)

        isvalid = any(result['isvalid'])

        return isvalid, result
    
    def predict_permite_pesquisa(self):

        files = self.files['html'][:self.keywords['max_files']]

        result = analyze_html(files, keyword_to_search=self.keywords['permite_pesquisa'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=1)

        return isvalid, result

    
    def predict(self):

        resultados = {
            'dados_de_remuneracao': { 'predict': False, 'explain': "Planilha consolidada: "},
        }

        # Agentes políticos
        isvalid_agentes_politicos, _ = self.predict_agentes_politicos()
        resultados['dados_de_remuneracao']['explain'] += self.explain(isvalid_agentes_politicos, 'agentes políticos')

        # Servidores efetivos
        isvalid_servidores_efetivos, _ = self.predict_servidores_efetivos()
        resultados['dados_de_remuneracao']['explain'] += self.explain(isvalid_servidores_efetivos, 'servidores efetivos')

        # Permite pesquisa
        isvalid_permite_pesquisa, _ = self.predict_permite_pesquisa()
        resultados['dados_de_remuneracao']['explain'] += self.explain(isvalid_permite_pesquisa, 'campo para pesquisa')


        if all([isvalid_agentes_politicos, 
            isvalid_servidores_efetivos, 
            isvalid_permite_pesquisa]):
            # Valida se todos são encontrados
            resultados['dados_de_remuneracao']['predict'] = True

        return resultados
        
    def explain(self, is_valid, description):
        if is_valid:
            result = f"""Encontrado {description}. """
        else:  
            result = f"""Não encontrado {description}. """
        return result