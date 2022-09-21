from src.validadores.utils import indexing
from src.validadores.utils import path_functions
from src.validadores.utils import path_functions
from src.validadores.utils.file_to_dataframe import get_df
from src.validadores.utils.check_df import check_all_values_of_column

class ValidadorDespesasComDiarias:

    def __init__(self, job_name, keywords):

        self.keywords = keywords
        files = indexing.get_files(keywords['search_term'], job_name, keywords_search=keywords['keywords_to_search'])
        files = path_functions.filter_paths(files, words=['despesas_com_diarias'])
        files = path_functions.agg_paths_by_type(files)
        self.files = files
        self.df = get_df(self.files, keywords['types'])

    # Número
    def predict_nome(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['nome'], typee='text')
        return isvalid, result

    # Cargo / Função
    def predict_cargo_funcao(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['cargo_funcao'], typee='text')
        return isvalid, result

    # Valores recebidos
    def predict_valores_recebidos(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['valores_recebidos'], typee='valor')
        return isvalid, result
    
    # Periodo da viagem
    def predict_periodo_da_viagem(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['periodo_da_viagem'], typee='text')
        return isvalid, result
    
    # Destino da viagem
    def predict_destino_da_viagem(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['destino_da_viagem'], typee='text')
        return isvalid, result
    
    # Motivo da viagem
    def predict_motivo_da_viagem(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['motivo_da_viagem'], typee='text')
        return isvalid, result

    # Numero de diarias
    def predict_numero_de_diarias(self):
        result, isvalid = check_all_values_of_column(self.df, self.keywords['numero_de_diarias'], typee='valor')
        return isvalid, result

    def predict(self):

        resultados_despesas_com_diarias = {
            'nome': {},
            'cargo_funcao': {},
            'valores_recebidos': {},
            'periodo_da_viagem': {},
            'destino_da_viagem': {},
            'motivo_da_viagem': {},
            'numero_de_diarias': {},
        }

        # Número
        isvalid, result = self.predict_nome()
        result_explain = self.explain(result, self.keywords['nome'], 'o nome do beneficiário')
        resultados_despesas_com_diarias['nome']['predict'] = isvalid
        resultados_despesas_com_diarias['nome']['explain'] = result_explain

        # Cargo / Função
        isvalid, result = self.predict_cargo_funcao()
        result_explain = self.explain(result, self.keywords['cargo_funcao'], 'o Cargo/Função')
        resultados_despesas_com_diarias['cargo_funcao']['predict'] = isvalid
        resultados_despesas_com_diarias['cargo_funcao']['explain'] = result_explain

        # Valores recebidos
        isvalid, result = self.predict_valores_recebidos()
        result_explain = self.explain(result, self.keywords['valores_recebidos'], 'os valores recebidos')
        resultados_despesas_com_diarias['valores_recebidos']['predict'] = isvalid
        resultados_despesas_com_diarias['valores_recebidos']['explain'] = result_explain

        # Periodo da viagem
        isvalid, result = self.predict_periodo_da_viagem()
        result_explain = self.explain(result, self.keywords['periodo_da_viagem'], 'o periodo da viagem')
        resultados_despesas_com_diarias['periodo_da_viagem']['predict'] = isvalid
        resultados_despesas_com_diarias['periodo_da_viagem']['explain'] = result_explain

        # Destino da viagem
        isvalid, result = self.predict_destino_da_viagem()
        result_explain = self.explain(result, self.keywords['destino_da_viagem'], 'a destino da viagem')
        resultados_despesas_com_diarias['destino_da_viagem']['predict'] = isvalid
        resultados_despesas_com_diarias['destino_da_viagem']['explain'] = result_explain
    
        # Motivo da viagem
        isvalid, result = self.predict_motivo_da_viagem()
        result_explain = self.explain(result, self.keywords['motivo_da_viagem'], 'a motivo da viagem')
        resultados_despesas_com_diarias['motivo_da_viagem']['predict'] = isvalid
        resultados_despesas_com_diarias['motivo_da_viagem']['explain'] = result_explain

        # Numero de diarias
        isvalid, result = self.predict_numero_de_diarias()
        result_explain = self.explain(result, self.keywords['numero_de_diarias'], 'o numero de diarias')
        resultados_despesas_com_diarias['numero_de_diarias']['predict'] = isvalid
        resultados_despesas_com_diarias['numero_de_diarias']['explain'] = result_explain

        return resultados_despesas_com_diarias
        
    def explain(self, result, column_name, description):
        result = f"Quantidade de entradas encontradas e analizadas: {len(result)}. Quantidade de entradas que possuem {description} do empenho válido: {sum(result['isvalid'])}"
        return result