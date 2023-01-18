from src.validadores.utils import indexing
from src.validadores.utils import check_df
from src.validadores.base import Validador
from src.validadores.utils.search_html import analyze_html
from src.municipio.manage_municipios import obter_url_portal

# Textos que validam o item: Texto padrão explicativo sobre a Lei de Acesso à Informação --
LEI_ACESSO_INFORMACAO_CONTEUDO = [
    'Cabe aos órgãos e entidades do poder público, observadas as normas e procedimentos específicos aplicáveis, assegurar',
    'conhecida como a Lei de Acesso à Informação',
    'Lei Federal 12.527',
    'Sistema Eletrônico de Serviço de Informações ao Cidadão',
    'A Lei de Acesso a Informações no',
    'em cumprimento a Lei nº 12.527',
    'Regula o acesso a informações previsto no inciso',
    'aumentando a transparência da gestão pública',
    'Leis que regem o Portal',
    'Regula o acesso a informações previsto',
    'Regulamenta o acesso à informação',
    'Dispõe sobre a disponibilização de informações',
    'Conheça essa legislação',
    'A Lei de Acesso a Informações no Brasil',
    'Institui como princípio fundamental que o acesso à informação pública é'
    # Possíveis acréscimos:
    # O acesso a informações públicas
    # ficou instituído
    # viabilizar o acesso
]

LINK_LEGISLACAO_FEDERAL = 'http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm'

LINK_LEGS_ESTADUAL = [
    'https://www.almg.gov.br/consulte/legislacao/completa/completa.html?num=45969&ano=2012&tipo=DEC',
    'https://www.transparencia.mg.gov.br/images/stories/decreto-45969.pdf',
    'http://www.transparencia.mg.gov.br/images/stories/decreto-45969.pdf'
]

URL_TRANSPARENCIA_MG = [
    'http://www.transparencia.mg.gov.br/',
    'www.transparencia.mg.gov.br',
    'https://www.transparencia.mg.gov.br/transferencia-de-impostos-a-municipios'
]

ACESSO_ILIMITADO = [
    'fazer cadastro',
    'necessario efetuar login',
    'clique aqui para fazer login',
    'clique aqui para fazer cadastro',
    'para baixar necessrio'
]

PERGUNTAS_FREQUENTES = ['FAQ', 'Perguntas Frequentes',
                        'perguntas frequentes', 'Perguntas', 'perguntas']


class ValidadorInformacoes(Validador):

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        self.job_name = job_name

    # 1 - Aba denominada “Transparência” no menu principal

    def predict_link_portal(self, keywords):

        html_files = indexing.get_files_html("Perguntas", self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        print('eita:',indexing.get_files("a", self.job_name, keywords_search=['a']))

        result = analyze_html(
            html_files, keyword_to_search=obter_url_portal(self.job_name))

        # Check result
        isvalid = check_df.files_isvalid(
            result, column_name='matches', threshold=1)

        return isvalid, result

    def explain_link_portal(self, df, column_name):
        result = "Explain - Quantidade de arquivos analizados: {} . Quantidade de páginas que possuem um link para o portal de transparencia do município: {}".format(
            len(df[column_name]), sum(df[column_name] > 0))
        return result

    # 2 - Texto padrão explicativo sobre a Lei de Acesso à Informação

    def predict_texto_explicativo(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        result = analyze_html(
            html_files, keyword_to_search=LEI_ACESSO_INFORMACAO_CONTEUDO)
        isvalid = check_df.files_isvalid(
            result, column_name='matches', threshold=1)
        return isvalid, result

    def explain_texto_explicativo(self, df, column_result):
        result = "Quantidade páginas que possuem texto explicativo sobre a Lei de Acesso a Informação: {}".format(
            sum(df[column_result]))
        return result

    # 3 - Link de acesso à legislação federal sobre a transparência (Lei nº 12.527/2011 e eventual legislação superveniente)

    def predict_legislacao_federal(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        predict, result = self.predict_link_em_pagina_html(
            html_files, LINK_LEGISLACAO_FEDERAL)
        return predict, result

    def explain_legislacao_federal(self, isvalid, result):
        if isvalid:
            result_explain = (
                f"O link da lei 12.527 foi encontrado em [{result['url']}] no(s) elemento(s): {result['macro']}")
        else:
            result_explain = " O link da lei 12.527 não foi encontrado."
        return result_explain

    # 4 - Link de acesso à leg Estadual sobre a transparência (Decreto Estadual nº 45.969/2012)-----------------

    def predict_legislacao_estadual(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        predict, result = self.predict_link_em_pagina_html(
            html_files, LINK_LEGS_ESTADUAL)
        return predict, result

    def explain_legislacao_estadual(self, isvalid, result):
        if isvalid:
            result_explain = (
                f"O link foi encontrado em encontrado em [{result['url']}] no(s) elemento(s): {result['macro']}")
        else:
            result_explain = (
                "O link do Decreto Estadual nº 45.969/2012 não foi encontrado.")
        return result_explain

    # 5 - Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)

    def predict_site_transparencia(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        predict, result = self.predict_link_em_pagina_html(
            html_files, URL_TRANSPARENCIA_MG)
        return predict, result

    def explain_site_transparencia(self, isvalid, result):
        if isvalid:
            result_explain = (
                f"O link foi encontrado em encontrado em [{result['url']}] no(s) elemento(s): {result['macro']}")
        else:
            result_explain = (
                "Não foi encontrado um link para a página de transparência de Minas Gerais.")
        return result_explain

    # 6 - Acesso ilimitado a todas as informações públicas do sítio eletrônico: o acesso sem cadastro ou ao fornecimento de dados pessoais

    def predict_acesso_ilimitado(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        result = analyze_html(
            html_files, keyword_to_search=ACESSO_ILIMITADO)
        isvalid = check_df.files_isvalid(
            result, column_name='matches', threshold=0)
        return not isvalid, result

    def explain_acesso_ilimitado(isvalid, df, column_name):
        if isvalid:
            result = "Não foi encontrada referência a fazer login ou cadastro no portal."
        else:
            result = "Explain - Quantidade de arquivos analizados: {}. Quantidade de aquivos que possuem referência fazer login ou cadastro: {}".format(
                len(df[column_name]), sum(df[column_name] > 0))
        return result

    # 7 - Link de respostas a perguntas mais frequentes da sociedade.

    def predict_perguntas_frequentes(self, keywords):

        html_files = indexing.get_files_html(keywords['search_term'], self.job_name,
                                             keywords_search=keywords['keywords_to_search'],
                                             filter_in_path=['acesso_a_informacao'])

        result = analyze_html(
            html_files, keyword_to_search=PERGUNTAS_FREQUENTES)
        isvalid = check_df.files_isvalid(
            result, column_name='matches', threshold=0)
        return isvalid, result

    def explain_perguntas_frequentes(isvalid, df, column_name):
        if isvalid:
            result = "Explain - Quantidade de arquivos analizados: {}. Quantidade de aquivos que possuem referência a Perguntas Frequentes: {}".format(
                len(df[column_name]), sum(df[column_name] > 0))
        else:
            result = "Nenhuma referência a Perguntas Frequentes foi encontrada nas páginas"
        return result

    def explain(self):
        pass

    def predict(self):

        resultados = {
            'link_portal': {},
            'texto_explicativo': {},
            'legislacao_federal': {},
            'legislacao_estadual': {},
            'site_transparencia': {},
            'acesso_ilimitado': {},
            'perguntas_frequentes': {},
        }

        # Aba denominada “Transparência” no menu principal
        isvalid, result = self.predict_link_portal(
            self.keywords['link_portal'])
        result_explain  = self.explain_link_portal(result, column_name='matches')
        resultados['link_portal']['predict'] = isvalid
        resultados['link_portal']['explain'] = result_explain

        # 2 - Texto padrão explicativo sobre a Lei de Acesso à Informação
        isvalid, result = self.predict_texto_explicativo(
            self.keywords['texto_explicativo'])
        result_explain = self.explain_texto_explicativo(result, 'matches')
        resultados['texto_explicativo']['predict'] = isvalid
        resultados['texto_explicativo']['explain'] = result_explain

        # 3 - Link de acesso à legislação federal sobre a transparência (Lei nº 12.527/2011 e eventual legislação superveniente)
        isvalid, result = self.predict_legislacao_federal(
            self.keywords['legislacao_federal'])
        result_explain = self.explain_legislacao_federal(isvalid, result)
        resultados['legislacao_federal']['predict'] = isvalid
        resultados['legislacao_federal']['explain'] = result_explain

        # 4 - Link de acesso à legislação federal sobre a transparência (Decreto Estadual nº 45.969/2012 e eventual legislação superveniente)
        isvalid, result = self.predict_legislacao_estadual(
            self.keywords['legislacao_estadual'])
        result_explain = self.explain_legislacao_estadual(isvalid, result)
        resultados['legislacao_estadual']['predict'] = isvalid
        resultados['legislacao_estadual']['explain'] = result_explain

        # 5 - Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)
        isvalid, result = self.predict_site_transparencia(
            self.keywords['site_transparencia'])
        result_explain = self.explain_site_transparencia(isvalid, result)
        resultados['site_transparencia']['predict'] = isvalid
        resultados['site_transparencia']['explain'] = result_explain

        # 6 - Acesso ilimitado a todas as informações públicas do sítio eletrônico: o acesso sem cadastro ou ao fornecimento de dados pessoais
        isvalid, result = self.predict_acesso_ilimitado(
            self.keywords['acesso_ilimitado'])
        result_explain = self.explain_acesso_ilimitado(result, 'matches')
        resultados['acesso_ilimitado']['predict'] = isvalid
        resultados['acesso_ilimitado']['explain'] = result_explain

        # 7 - Link de respostas a perguntas mais frequentes da sociedade.
        isvalid, result = self.predict_perguntas_frequentes(
            self.keywords['perguntas_frequentes'])
        result_explain = self.explain_perguntas_frequentes(result, 'matches')
        resultados['perguntas_frequentes']['predict'] = isvalid
        resultados['perguntas_frequentes']['explain'] = result_explain

        return resultados
