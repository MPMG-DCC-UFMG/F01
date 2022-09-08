from src.validadores.utils import read
from abc import ABC, abstractmethod
from src.validadores.utils.path_functions import get_url
from src.validadores.utils.search_html import search_links

class Validador(ABC):
    """
    Validador base de todos validadores do projeto.
    """

    @abstractmethod
    def explain(self, df, column_name):         
        """
        Responsável por resumir em uma string o resultado da validação.
        
        Parameters
        ----------
        df : dataframe resultante da validação
        column_name : str
            
        Returns
        -------
        str
            uma string resumindo o resultado da validação.        
        """
        pass
    
    def predict_link_em_pagina_html(self, html_files, links):

        """
        Método que valida um link em alguma página html.

        procura um dos links 
        Responsável por resumir em uma string o resultado da validação. 
        
        Parameters:

        * html_files : lista de strings
            Caminhos para arquivos 'html'.
        * links : lista de strings
            Links procurados.
            
        Returns:

        * predict: boleano
            True ou False, sendo o resultado da validação. 
        * result: dicionário, 
            Contém: - file_name (arquivo que o link foi encontrado)  
                    - url (em que o link foi encontrado, caso não disponível (por falha no arquivo 'file_description.json'), o arquivo)  
                    - macro (elemento em que o link foi encontradio)

        Critério
        -------
        Predict true: caso encontre algum dos links recebidos em alguma página(html_files), retorna a primera delas.
        Predict false: caso não encontre nenhum dos links recebidos em nenhuma página(html_files), retorna a primera delas.
        """

        result = {
            'url': None,
            'macro': None,
        }

        for filename in html_files:
            markup = read.read_html(filename)
            result['macro'] = search_links(markup, links)

            if len(result['macro']):
                result['url'] = get_url(filename)
                return True, result
        
        # Se não encontrou em nenhum html_file
        return False, result

