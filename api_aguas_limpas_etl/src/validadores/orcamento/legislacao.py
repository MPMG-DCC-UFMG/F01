from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.search_html import analyze_html

class ValidadorLegislacao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        self.job_name = job_name

    def predict_item(self, item):
        keywords = self.keywords[item]
        files = indexing.get_files(keywords['search_term'], self.job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['orcamento'])
        files = path_functions.agg_paths_by_type(files)

        result = {"documentos":{}, "paginas":{}}

        result['documentos'] = len(files['pdf'])
        result_html = analyze_html(files['html'], keyword_to_search=keywords['keyword_check'])

        result['paginas'] = sum(result_html['matches'])
        isvalid = result['documentos'] > 0 or result['paginas'] > 0
        return isvalid, result   

    def explain(self, result, descricao):
        result = f"""Foram encontrados {result["documentos"]} pdfs na coleta que mencionam {descricao} e {result["paginas"]} menções em páginas html."""
        return result

    def predict(self):

        resultados = {
            'lei_orcamentaria_anual': {},
            'lei_diretrizes_orcamentarias': {},
            'plano_plurianual': {},
            'informacoes_audiencias_publicas': {},
        }

        # Lei Orçamentária Anual
        isvalid, result = self.predict_item('lei_orcamentaria_anual')
        result_explain = self.explain(result, 'Lei Orçamentária Anual')
        resultados['lei_orcamentaria_anual']['predict'] = isvalid
        resultados['lei_orcamentaria_anual']['explain'] = result_explain

        # Lei de Diretrizes Orçamentárias
        isvalid, result = self.predict_item('lei_diretrizes_orcamentarias')
        result_explain = self.explain(result, 'Lei de Diretrizes Orçamentárias')
        resultados['lei_diretrizes_orcamentarias']['predict'] = isvalid
        resultados['lei_diretrizes_orcamentarias']['explain'] = result_explain

        # Plano Plurianual
        isvalid, result = self.predict_item('plano_plurianual')
        result_explain = self.explain(result, 'Plano Plurianual')
        resultados['plano_plurianual']['predict'] = isvalid
        resultados['plano_plurianual']['explain'] = result_explain

        # Ata / vídeo / informações sobre as audiências públicas obrigatórias
        isvalid, result = self.predict_item('informacoes_audiencias_publicas')
        result_explain = self.explain(result, 'Ata / vídeo / informações sobre as audiências públicas obrigatórias')
        resultados['informacoes_audiencias_publicas']['predict'] = isvalid
        resultados['informacoes_audiencias_publicas']['explain'] = result_explain

        return resultados
