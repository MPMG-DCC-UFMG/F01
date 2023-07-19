import os
from src import db
import pandas as pd
from src.checklist.models import Tag, Subtag, Item

def get_all_itens():
    itens = Item.query.all()
    return itens

def get_tag_by_name_in_github(nome_da_tag):
    # Adaptação para os nomes de tag que estão diferentes no githubm eles são:
    nome_da_tag_no_git_hub = {
        'licitacao': "licitacoes",
        'servidores': "servidores_publicos",
    }

    if (nome_da_tag in nome_da_tag_no_git_hub):
        nome_da_tag = nome_da_tag_no_git_hub[nome_da_tag]

    tag = Tag.query.filter_by(nome=nome_da_tag).first()
    if tag is None:
        return None
    return tag.nome


def get_tag_id_by_name(nome_da_tag):
    tag = Tag.query.filter_by(nome=nome_da_tag).first()
    if tag:
        return tag.id
    else:
        return None

def get_tag_itens(nome_da_tag):
    tag = Tag.query.filter_by(nome=nome_da_tag).first()
    if tag:
        return tag.itens
    else:
        return None

def get_sub_tag_itens(nome_da_subtag):
    subtag = Subtag.query.filter_by(nome=nome_da_subtag).first()
    if subtag:
        return subtag.itens
    else:
        return None

def get_sub_tag(nome_da_subtag):
    subtag = Subtag.query.filter_by(nome=nome_da_subtag).first()
    return subtag

def get_item(subtag_id, nome_do_item):
    itens = Item.query.filter_by(subtag_id=subtag_id, abreviacao=nome_do_item).first()
    return itens

def formatar_nome(nome):
    ori = "àãâáíẽéêóôõçú "
    rep = "aaaaioeeooocu_"
    nome_formatado = nome.lower().strip()
    for i in range(len(ori)):
        if ori[i] in nome_formatado:
            nome_formatado = nome_formatado.replace(ori[i], rep[i])

    nome_formatado = nome_formatado.replace("(", "").replace(")", "")
    return nome_formatado

def carregar_checklist():

    # Item.query.delete()
    # Subtag.query.delete()
    # Tag.query.delete()

    # 1) Cadastra as tags, subtags e itens de acordo com a checklist ('lista_exigencias.csv')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/lista_exigencias.csv')

    # Cadastrando tags
    tags = df['tag'].unique()
    tags = [formatar_nome(tag) for tag in tags]

    for tag in tags:
        resultado_consulta = Tag.query.filter_by(nome=tag).all()
        if len(resultado_consulta) != 0:
            print(f"Tag {tag} já cadastrada.")
        else:
            tag = Tag(nome=tag)
            db.session.add(tag)

    db.session.commit()

    # Cadastrando sub-tags
    for _, row in df.iterrows():
        nome_da_tag = formatar_nome(row['tag'])
        nome_da_sub_tag = formatar_nome(row['sub-tag'])

        tag = Tag.query.filter_by(nome=nome_da_tag).first()
        resultado_consulta = Subtag.query.filter_by(
            nome=nome_da_sub_tag, tag_id=tag.id).all()

        if len(resultado_consulta) != 0:
            print(f"Subtag \"{nome_da_sub_tag}\" já cadastrado.")
        else:
            sub_tag = Subtag(nome=nome_da_sub_tag, tag_id=tag.id)
            db.session.add(sub_tag)

    db.session.commit()

    # Cadastrando itens
    for _, row in df.iterrows():
        nome_da_tag = formatar_nome(row['tag'])
        nome_da_sub_tag = formatar_nome(row['sub-tag'])
        nome_do_item = formatar_nome(row['info'])
        try:
            abreviacao = formatar_nome(row['abreviacao'])
        except AttributeError:
            abreviacao = None

        tag = Tag.query.filter_by(nome=nome_da_tag).first()
        sub_tag = Subtag.query.filter_by(nome=nome_da_sub_tag).first()

        resultado_consulta = Item.query.filter_by(
            nome=nome_do_item, tag_id=tag.id, subtag_id=sub_tag.id, abreviacao=abreviacao).all()
        if len(resultado_consulta) != 0:
            print(f"Item \"{nome_do_item}\" já cadastrado.")
        else:
            print(f"Item \"{nome_do_item}\" cadastrado.")
            item = Item(nome=nome_do_item, tag_id=tag.id, subtag_id=sub_tag.id, abreviacao=abreviacao)
            db.session.add(item)

    db.session.commit()