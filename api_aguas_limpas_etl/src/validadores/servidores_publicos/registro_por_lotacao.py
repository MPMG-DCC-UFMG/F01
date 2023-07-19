
from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column
from src.validadores.utils.check_df import search_in_column

class ValidadorRegistroPorLotacao:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['servidores_publicos','servidores'])
        self.files = path_functions.agg_paths_by_type(files)
        self.df = get_df(self.files, keywords['types'])
        # print(len(self.files), self.df.columns)

    def predict_matricula(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['matricula'], typee='text')
        return isvalid, result

    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    def predict_cargo_funcao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo_funcao'], typee='text')
        return isvalid, result
    
    def predict_remuneracao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['remuneracao'], typee='text')
        return isvalid, result
    
    def predict_abate_teto(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['abate_teto'], typee='text')
        return isvalid, result

    def predict_tipo_de_vinculo(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['tipo_de_vinculo'], typee='text')
        return isvalid, result

    
    def predict(self):
        # Registro realizado por 
        # lotação, matrícula, nome, cargo, remuneração, abate teto, remuneração retirando o abate teto e o tipo de vínculo 
        # (detalhar se faltou alguma destas informações)

        resultados = {
            'registro_por_lotacao': { 'predict': False, 'explain': "Registro por lotação não encontrado."},
        }

        # - validar se existe uma coluna "lotação"

        _, isvalid_column = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')

        if isvalid_column:
        # - validar os itens
            isvalid = {}
            # Matrícula
            isvalid['matricula'], _ = self.predict_matricula()
            result_explain = self.explain('matrícula')
            if not isvalid['matricula']:
                resultados['registro_por_lotacao']['explain'] += result_explain

            # Nome
            isvalid['nome'], _ = self.predict_nome()
            result_explain = self.explain('nome')
            if not isvalid['nome']:
                resultados['registro_por_lotacao']['explain'] += result_explain

            # Cargo/Função
            isvalid['cargo_funcao'], _ = self.predict_cargo_funcao()
            result_explain = self.explain('cargo/função')
            if not isvalid['cargo_funcao']:
                resultados['registro_por_lotacao']['explain'] += result_explain

            # Remuneração
            isvalid['remuneracao'], _ = self.predict_remuneracao()
            result_explain = self.explain('remuneração')
            if not isvalid['remuneracao']:
                resultados['registro_por_lotacao']['explain'] += result_explain

            # Abate teto
            isvalid['abate_teto'], _ = self.predict_abate_teto()
            result_explain = self.explain('abate teto')
            if not isvalid['abate_teto']:
                resultados['registro_por_lotacao']['explain'] += result_explain

            # Tipo de vínculo
            isvalid['tipo_de_vinculo'], _ = self.predict_tipo_de_vinculo()
            result_explain = self.explain('tipo de vínculo')
            if not isvalid['tipo_de_vinculo']:
                resultados['registro_por_lotacao']['explain'] += result_explain
        
        if isvalid_column:
            resultados['registro_por_lotacao']['predict'] = True
    
        return resultados
        
    def explain(self, description):
        result = f"""Não possui {description}. """
        return result