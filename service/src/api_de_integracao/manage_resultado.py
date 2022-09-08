from src import db
from src.api_de_integracao.models import Resultado


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
