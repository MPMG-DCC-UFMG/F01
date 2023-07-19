"""
Expose public exceptions & warnings
"""

class ErroValidacao(Exception):
    """
    Erros de validação
    """
    
class FileDescriptionVazio(ErroValidacao):
    """
    É lançada quando o arquivo file_description está vazio
    """