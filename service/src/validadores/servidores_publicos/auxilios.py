
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.check_df import search_in_column
from src.validadores.utils.check_df import infos_isvalid
from src.validadores.utils.search_html import analyze_html

class ValidadorAuxilios:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        # print(self.files)
        # print(len(self.files), self.df.columns)

    # Verbas indenizatórias
    def predict_verbas_indenizatorias(self):
        result = []
        return False, result
    
    def predict_verbas_indenizatorias(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)

        # Check result 
        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result 

    # Ajuda de custos
    def predict_ajuda_de_custos(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)

        #Check result 
        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result 

    # Jetons
    def predict_jetons(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)

        #Check result 
        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result 

    # Vantagens pecuniárias
    def predict_vantagens_pecuniarias(self, keyword_check):

        # Analyze 
        files = self.files['html']
        result = analyze_html(files, keyword_to_search=keyword_check)

        # Check result 
        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result 
    
    def predict(self):

        resultados = {
            'auxilios': { 'predict': False, 'explain': "Registro de auxílios."},
        }

        # Verbas indenizatórias
        isvalid_verbas_indenizatorias, _ = self.predict_verbas_indenizatorias(self.keywords['verbas_indenizatorias'])
        resultados['auxilios']['explain'] += self.explain(isvalid_verbas_indenizatorias, 'verbas indenizatórias')

        # Ajuda de custos
        isvalid_ajuda_de_custos, _ = self.predict_ajuda_de_custos(self.keywords['ajuda_de_custos'])
        resultados['auxilios']['explain'] += self.explain(isvalid_ajuda_de_custos, 'ajuda de custos')

        # Jetons
        isvalid_jetons, _ = self.predict_jetons(self.keywords['jetons'])
        resultados['auxilios']['explain'] += self.explain(isvalid_jetons, 'jetons')

        # Vantagens pecuniárias
        isvalid_vantagens_pecuniarias, _ = self.predict_vantagens_pecuniarias(self.keywords['vantagens_pecuniarias'])
        resultados['auxilios']['explain'] += self.explain(isvalid_vantagens_pecuniarias, 'vantagens pecuniárias')

        if any([isvalid_verbas_indenizatorias, 
                isvalid_ajuda_de_custos, 
                isvalid_jetons, 
                isvalid_vantagens_pecuniarias]):
            # Qualquer um é um registro de auxilio, então pelo menos um ja valida
            # o item para TRUE
            resultados['auxilios']['predict'] = True

        return resultados
        
    def explain(self, is_valid, description):
        if is_valid:
            result = f"""Encontrado {description}. """
        else:  
            result = f"""Não encontrado {description}. """
        return result



# vantagens pecuniárias
# indenizações, gratificações e adicionais.