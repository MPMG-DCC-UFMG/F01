
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorProventosDePensao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])

    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    def predict_cargo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo'], typee='text')
        return isvalid, result
    
    def predict_remuneracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao'], typee='text')
        return isvalid, result
    
    def predict_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['abate_teto'], typee='text')
        return isvalid, result

    def predict_remuneracao_retirando_o_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao_sem_abate_teto'], typee='text')
        return isvalid, result
    
    def predict_tipo_de_vinculo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['tipo_de_vinculo'], typee='text')
        return isvalid, result

    def predict(self):

        resultados = {
            'proventos_de_pensao': { 'predict': False, 'explain': "Registro dos proventos de pensão."},
        }
        # - Filtar os que são aposentados
        # Como pode ser que a mesma pessoa esteja com os dados divididos, em mais de uma linha, ex:

        #     FileName        CPF             LOTAÇÃO	     SITUAÇÃO	  NOME DO SERVIDOR         CARGO
        #  a2sa1d2a.html                      Aposentados	 Inativo	                           AG.ADMINISTRATIVO II
        #  a2sa1d2a.html      ***.264.556-**                              EDSON SILVA

        # Vamos Manter todas as linhas que contêm a raiz 'pens' na coluna e, além disso,
        # manter todas as linhas que têm o mesmo valor na coluna 'FileName' dessas linhas.

        try:
            column_to_filter = self.keywords['pensao']
            mask = self.df[column_to_filter].str.contains('pens', regex=True, na=False, case=False)
            file_names_to_keep = self.df[mask]['FileName'].unique()
            mask = mask | self.df['FileName'].isin(file_names_to_keep)
            self.df = self.df[mask]
        except KeyError:
            return resultados

        # - validar os itens

        # Nome
        isvalid_nome, _ = self.predict_nome()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_nome, 'nome')

        # Cargo
        isvalid_cargo, _ = self.predict_cargo()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_cargo, 'cargo')

        # Remuneração
        isvalid_remuneracao, _ = self.predict_remuneracao()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_remuneracao, 'remuneração')

        # Abate teto
        isvalid_abate_teto, _ = self.predict_abate_teto()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_abate_teto, 'abate teto')

        # Remuneração retirando o abate teto
        isvalid_retirando_o_abate_teto, _ = self.predict_remuneracao_retirando_o_abate_teto()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_retirando_o_abate_teto, 'remuneração retirando o abate teto')

        # Tipo de vínculo
        isvalid_tipo_de_vinculo, _ = self.predict_tipo_de_vinculo()
        resultados['proventos_de_pensao']['explain'] += self.explain(isvalid_tipo_de_vinculo, 'tipo de vínculo')

        if any([isvalid_nome, 
                isvalid_cargo, 
                isvalid_remuneracao, 
                isvalid_abate_teto,
                isvalid_retirando_o_abate_teto,
                isvalid_tipo_de_vinculo]):
            # Se pelo menos um ja valida o item para TRUE, detalha se faltou algum no explain.
            resultados['proventos_de_pensao']['predict'] = True

        return resultados
        
    def explain(self, is_valid, description):
        if is_valid:
            result = f"""Encontrado {description}. """
        else:  
            result = f"""Não encontrado {description}. """
        return result