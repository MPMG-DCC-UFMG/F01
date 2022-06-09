import re
from utils.file_to_df import get_df
from utils import indexing, path_functions
from utils.check_df import check_all_values_of_column, contains_keyword, infos_isvalid
from utils.search_html import analyze_html

def analyze_inexibilidade (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é inexibilidade
    """
    try:
        if re.search("inexigibilidade", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False
    except TypeError:
        return False

def analyze_dispensa (value, column_name):
    """
    Verifica se existem licitações cuja modelidade é dispensa
    """
    try:
        if re.search("dispensa", value[column_name], re.IGNORECASE) != None:
            return True
        else: 
            return False
    except TypeError:
        return False


class ValidadorRegistroDosProcedimentos:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], keywords['num_matches'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['licitacao'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
    
    def predict_inexibilidade(self):
        result = {'inexigibilidade': []}

        if self.df is None: return False, result

        for _, value in self.df.iterrows():
            result['inexigibilidade'].append(analyze_inexibilidade (value, self.keywords['coluna_modalidade']))

        isvalid = infos_isvalid(result, column_name='inexigibilidade', threshold=0)
            
        return isvalid, result

    def predict_dispensa(self):
        result = {'dispensa': []}

        if self.df is None: return False, result

        for _, value in self.df.iterrows():
            result['dispensa'].append(analyze_dispensa (value, self.keywords['coluna_modalidade']))

        isvalid = infos_isvalid(result, column_name='dispensa', threshold=0)
        return isvalid, result
    
    def predict_ordem(self):

        files = self.files['html']

        result = analyze_html(files, keyword_to_search=self.keywords['ordem'])

        isvalid = infos_isvalid(result, column_name='matches', threshold=0)

        return isvalid, result
    
    def predict(self):

        resultados = {'inexigibilidade_e_dispensa': {},}

        # Inexibilidade
        isvalid_inexibilidade, result_inexibilidade = self.predict_inexibilidade()

        # Dispensa
        isvalid_dispensa, result_dispensa = self.predict_dispensa()

        # Ordem
        predict_ordem, _ = self.predict_ordem()

        isvalid = isvalid_inexibilidade and isvalid_dispensa and predict_ordem
        result = result_inexibilidade['inexigibilidade'] + result_dispensa['dispensa']

        result_explain = self.explain(result, predict_ordem)
        resultados['inexigibilidade_e_dispensa']['predict'] = isvalid
        resultados['inexigibilidade_e_dispensa']['explain'] = result_explain

        return resultados
        
    def explain(self, result, predict_ordem):
        numero_de_entradas = len(result)

        result = f"""Quantidade de entradas encontradas e analizadas: {numero_de_entradas}.
        Quantidade de entradas que possuem a modalidade dispensa ou inexigibilidade : {sum(result)}. """

        if predict_ordem:
            result += "É possível ordenar os procedimentos"
        else:
           result += "Não é possível ordenar os procedimentos"
        return result