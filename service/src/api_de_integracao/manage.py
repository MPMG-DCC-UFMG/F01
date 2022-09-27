from glob import escape
import json
from src import db
from src.checklist.manage import get_item, get_sub_tag, get_tag_itens
from src.api_de_integracao.models import Resultado
from src.api_de_integracao.resposta import Resposta
from enum import Enum


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


def get_resposta_por_erro_de_validacao(erro_de_coleta):

    mapeamento_erro_resposta = {
        'ainda não validado': Resposta.ITEM_NAO_DISPONIVEL,
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

    if resultado is not None:

        resultado = {resultado.item_id: {
            'codigo_resposta': resultado.codigo_resposta,
            'justificativa': resultado.justificativa}
        }

    return resultado


def salvar_resultado(municipio_id, item_id, resposta):

    codigo_resposta = resposta.get_codigo_resposta()
    justificativa = resposta.get_justificativa()

    resultado_atual = Resultado.query.filter_by(
        municipio_id=municipio_id, item_id=item_id).first()

    if resultado_atual is not None:
        resultado_atual.codigo_resposta = codigo_resposta
        resultado_atual.justificativa = justificativa
        resultado_atualizado = resultado_atual
        db.session.commit()
        return resultado_atualizado

    else:
        novo_resultado = Resultado(item_id=item_id,
                                   municipio_id=municipio_id,
                                   codigo_resposta=codigo_resposta,
                                   justificativa=justificativa)
        db.session.add(novo_resultado)
        db.session.commit()
        return novo_resultado


def salvar_resultado_de_json(municipio_id, resultado_json):

    # nome_da_tag_no_git_hub = {
    #     'licitacao': "licitacoes",
    #     'servidores': "servidores_publicos",
    # }

    # if (nome_da_tag in nome_da_tag_no_git_hub):
    #     nome_da_tag = nome_da_tag_no_git_hub[nome_da_tag]

    for tag, resultado_por_tag in resultado_json.items():

        if resultado_por_tag is None:
            itens = get_tag_itens(tag)
            resposta = get_resposta_por_erro_de_validacao("ainda não validado")
            for item in itens:
                salvar_resultado(municipio_id=municipio_id,
                                 item_id=item.id, resposta=resposta)

            continue

        for subtag, resultado_por_subtag in resultado_por_tag.items():

            for item_apelido, resultado_do_item in resultado_por_subtag.items():

                item = get_item(get_sub_tag(subtag).id, item_apelido)

                if resultado_do_item['predict']:
                    resposta = Resposta.TRUE
                else:
                    resposta = Resposta.FALSE
                resposta.set_justificativa(resultado_do_item['explain'])

                salvar_resultado(municipio_id=municipio_id,
                                 item_id=item.id, resposta=resposta)


def formatar_nome(nome):
    ori = "àãâáíẽéêóôõçú "
    rep = "aaaaioeeooocu_"
    nome_formatado = nome.lower().strip()
    for i in range(len(ori)):
        if ori[i] in nome_formatado:
            nome_formatado = nome_formatado.replace(ori[i], rep[i])

    nome_formatado = nome_formatado.replace("(", "").replace(")", "")
    return nome_formatado


def get_github_token():
    with open('../service/github_token.json', 'r') as myfile:
        data = myfile.read()
        token = json.loads(data)
        return token['github_token']
