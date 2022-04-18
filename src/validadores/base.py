from abc import ABC, abstractmethod

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
    
    