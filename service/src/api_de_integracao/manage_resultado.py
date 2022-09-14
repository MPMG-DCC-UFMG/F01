from src import db
from enum import Enum
from src.api_de_integracao.models import Resultado

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

def procurar_resultado(municipio_id, item_id=None):

    # Retorna todos os resultados do mesmo município
    if item_id is None:

        resultado = [{resultado.item_id: resultado.resposta}
                     for resultado in Resultado.query.filter_by(municipio_id=municipio_id).all()]
        return resultado

    resultado = Resultado.query.filter_by(
        municipio_id=municipio_id, item_id=item_id).first()
    return resultado


def salvar_resultado(resultado, municipio_id, item_id):

    resultado_atual = procurar_resultado(municipio_id, item_id)

    if resultado_atual is not None:
        return resultado_atual

    else:
        novo_resultado = Resultado(item_id=item_id,
                                   municipio_id=municipio_id,
                                   resposta=resultado)
        db.session.add(novo_resultado)
        db.session.commit()
        return novo_resultado


def formatar_nome(nome):
    ori = "ãâáíẽéêóôõçú "
    rep = "aaaioeeooocu_"
    nome_formatado = nome.lower()
    for i in range(len(ori)):
        if ori[i] in nome_formatado:
            nome_formatado = nome_formatado.replace(ori[i], rep[i])
    return nome_formatado