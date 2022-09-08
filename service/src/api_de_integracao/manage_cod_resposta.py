from enum import Enum

class Resposta(Enum):
    OK = "Item validado com sucesso" 
    ITEM_NAO_DISPONIVEL = "Erro generico para item"  
    MUNICIPIO_NAO_DISPONIVEL = "Erro generico para municipi"  
    NAO_COLETADO = "Item nao encontrado no portal de transparencia"
    NAO_COLETADO_ERRO_TIMEOUT = "Item encontrado, mas houve erro de timeout na coleta"
    NAO_VALIDADO = "Validacao informou que o item coletado nao atende aos requisitos"
    AINDA_NAO_VALIDADO = "Validacao informou que o item coletado nao atende aos requisitos"

    def to_dict(self):
        return {'resposta': self.name, 'justificativa': self.value}