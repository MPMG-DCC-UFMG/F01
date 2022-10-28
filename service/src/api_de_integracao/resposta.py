from enum import Enum

class Resposta(Enum):
    # "Name" sera' o código e "Value" a justificativa

    # Github
    ISSUE_BLOQUEADA = "Issue bloqueada por algum motivo"
    NAO_COLETAVEL_REDIRECIONADO = "Dados são encontrados somente fora do padrão do template"
    NAO_COLETAVEL_TIMEOUT = "Dados não coletados devido a erro de Timeout"
    NAO_LOCALIZADO = "Dados não foram localizados no template"
    NAO_LOCALIZADO_LINK_INCORRETO = "Dados inacessíveis pelos portais do template"

    # Validação
    ITEM_NAO_DISPONIVEL = "Item ainda não validado"

    ERRO_VALIDADO = "Validação informou que o item coletado nao atende aos requisitos"
    OK_VALIDADO = "Item validado com sucesso"


    # Outros erros
    MUNICIPIO_NAO_DISPONIVEL = "Municipio inválido ou não abordado"

    def to_dict(self):
        try:
            return {'codigo': self.name, 'justificativa': self.value + ". " + self.explain}
        except AttributeError:
            return {'codigo': self.name, 'justificativa': self.value}

    def get_codigo_resposta(self):
        return self.name
  
    def get_justificativa(self):
        try:
            return self.value  + ". " +  self.explain
        except AttributeError:
            return self.value

    def set_justificativa(self, justificativa):
        self.explain = justificativa