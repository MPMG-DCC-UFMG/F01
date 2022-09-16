from src import db
from enum import Enum
from src.api_de_integracao.models import Resultado


class Resposta(Enum):

    # Github
    ISSUE_BLOQUEADA = "Issue bloqueada por algum motivo"
    NAO_COLETAVEL_REDIRECIONADO = "Dados são encontrados somente fora do padrão do template"
    NAO_COLETAVEL_TIMEOUT = "Dados não coletados devido a erro de Timeout"
    NAO_LOCALIZADO = "Dados não foram localizados no template"
    NAO_LOCALIZADO_LINK_INCORRETO = "Dados inacessíveis pelos portais do template"

    # Validação
    ITEM_NAO_DISPONIVEL = "Item ainda não validado"
    FALSE = "Validacao informou que o item coletado nao atende aos requisitos"
    TRUE = "Item validado com sucesso"

    # Outros erros
    MUNICIPIO_NAO_DISPONIVEL = "Municipio não abordado"

    def to_dict(self):
        return {'resposta': self.name, 'justificativa': self.value}

    def get_codigo_resposta(self):
        return self.name

    def get_justificativa(self):
        return self.value


def is_issue_erro(nome_da_label):

    erros_de_coleta_github = [
        'bloqueada'
        'não-coletável-redirecionado',
        'não-coletável-timeout',
        'não-localizado',
        'não-localizado-link-incorreto'
    ]

    for erro_de_coleta_github in erros_de_coleta_github:
        if nome_da_label == erro_de_coleta_github:
            return True

    return False


def get_resposta_por_erro_de_coleta(erro_de_coleta):

    mapeamento_erro_resposta = {
        'bloqueada': Resposta.ISSUE_BLOQUEADA,
        'não-coletável-redirecionado': Resposta.NAO_COLETAVEL_REDIRECIONADO,
        'não-coletável-timeout': Resposta.NAO_COLETAVEL_TIMEOUT,
        'não-localizado': Resposta.NAO_LOCALIZADO,
        'não-localizado-link-incorreto': Resposta.NAO_LOCALIZADO_LINK_INCORRETO
    }
    return mapeamento_erro_resposta[erro_de_coleta]


def procurar_resultado(municipio_id, item_id=None):

    # Retorna todos os resultados do mesmo município
    if item_id is None:

        resultado = [
            {resultado.item_id: {
                'codigo_resposta': resultado.codigo_resposta,
                'justificativa': resultado.justificativa}
             }
            for resultado in Resultado.query.filter_by(municipio_id=municipio_id).all()
        ]

        return resultado

    resultado = Resultado.query.filter_by(
        municipio_id=municipio_id, item_id=item_id).first()

    resultado = {resultado.item_id: {
        'codigo_resposta': resultado.codigo_resposta,
        'justificativa': resultado.justificativa}
    }

    return resultado


def salvar_resultado(municipio_id, item_id, codigo_resposta, justificativa):

    resultado_atual = procurar_resultado(municipio_id, item_id)

    if resultado_atual is not None:
        return resultado_atual

    else:
        novo_resultado = Resultado(item_id=item_id,
                                   municipio_id=municipio_id,
                                   codigo_resposta=codigo_resposta,
                                   justificativa=justificativa)
        db.session.add(novo_resultado)
        db.session.commit()
        return novo_resultado


def formatar_nome(nome):
    ori = "àãâáíẽéêóôõçú "
    rep = "aaaaioeeooocu_"
    nome_formatado = nome.lower().strip()
    for i in range(len(ori)):
        if ori[i] in nome_formatado:
            nome_formatado = nome_formatado.replace(ori[i], rep[i])
    return nome_formatado
