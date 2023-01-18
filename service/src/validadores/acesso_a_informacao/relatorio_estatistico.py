from src.validadores.utils import indexing
from src.validadores.utils import check_df
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

# Relatório estatístico (Divulgação de relatório de atendimentos)
class ValidadorRelatorioEstatistico:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['relatorio_estatistico'])
        self.files = path_functions.agg_paths_by_type(files)

    # Quantidade de pedidos recebidos
    def predict_quantidade(self):

        result = analyze_html(self.files['html'], keyword_to_search=self.keywords['quantidade'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
        return isvalid, result
    
    # Quantidade e/ou percentual de pedidos atendidos
    def predict_atendidos(self):
        result = analyze_html(self.files['html'], keyword_to_search=self.keywords['atendidos'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
        return isvalid, result

    # Quantidade e/ou percentual de pedidos indeferidos
    def predict_indeferidos(self):
        result = analyze_html(self.files['html'], keyword_to_search=self.keywords['indeferidos'])
        isvalid = check_df.files_isvalid(result, column_name='matches', threshold=0)
        return isvalid, result

    def explain(self, result, descricao):
        if result.size:  
            result_explain = f"Referências a {descricao} de pedidos de atendimentos foram encontrados."
        else:     
            result_explain = f"Referências a {descricao} de pedidos de atendimentos não foram encontrados."
        return result_explain
    
    def predict(self):

        resultados = {
            'quantidade': {},
            'atendidos': {},
            'indeferidos': {},
        }

        resultados['quantidade']['predict'], result = self.predict_quantidade()
        resultados['quantidade']['explain'] = self.explain(result, "quantidade")

        resultados['atendidos']['predict'], result = self.predict_atendidos()
        resultados['atendidos']['explain'] = self.explain(result, "quantidade atendida")

        resultados['indeferidos']['predict'], result = self.predict_indeferidos()
        resultados['indeferidos']['explain'] = self.explain(result, "quantidade indeferida")

        return resultados
        