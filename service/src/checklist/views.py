import os
from src import db
import pandas as pd
from flask import jsonify
from flask import Blueprint
from flask import Blueprint
from src.checklist.manage import get_tag_itens
from src.checklist.models import Tag, Subtag, Item
from src.api_de_integracao.manage import formatar_nome

checklist = Blueprint('checklist', __name__)


@checklist.route('/cadastrar_checklist', methods=['POST', 'GET'])
def cadastrar_checklist():
    Tag.query.delete()
    Subtag.query.delete()
    Item.query.delete()

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

    return jsonify('ok')


@checklist.route('/teste', methods=['POST', 'GET'])
def teste():
    nome_da_tag = 'concursos_publicos'
    tag = Tag.query.filter_by(nome=nome_da_tag).first()
    print(tag.itens)
    return jsonify('ok')