from src.validadores.utils import read
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html
from src.validadores.utils.search_html import search_links

class ValidadorDadosAbertos:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['dados_abertos'])
        self.files = path_functions.agg_paths_by_type(files)

    # Publica na internete relação das bases de dados abertos do município ou do estado

    def predict_dados_abertos(self):

        result = 0

        for path in self.files['html']:
            soup = read.read_html(path)
            macro = search_links(soup, self.keywords['url_keyword'])
            if macro:
                result += 1

        if result >= 1:
            predict = True
        else:
            predict = False

        return predict, result

    def explain_dados_abertos(isvalid, result):
        if isvalid:  
            result_explain = f"Referências a publicações de dados abertos foram encontrados em {result} página."

        else:     
            result_explain = ("Referências a publicações de dados abertos não foram encontrados.")

        return result_explain
    
    def predict(self):

        resultados = {
            'dados_abertos': {},
        }

        resultados['dados_abertos']['predict'], result = self.predict_dados_abertos()
        resultados['dados_abertos']['explain'] = self.explain_dados_abertos(result)

        return resultados
        