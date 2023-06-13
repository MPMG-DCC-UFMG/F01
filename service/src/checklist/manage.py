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