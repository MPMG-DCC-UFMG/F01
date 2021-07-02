import codecs
import os
import sys
import constant
from bs4 import BeautifulSoup

est_org_dict = {
    "title": None,
    "url": None
}
link_legislacao_dict = {
    "title": None,
    "url": None
}
checklist_info_institucionais_percent = {
    'competência': 0,
    'endereço': 0,
    'telefone': 0,
    'horário_atendimento': 0
}
checklist_info_institucionais = {
    'competência': False,
    'endereço': False,
    'telefone': False,
    'horário_atendimento': False
}
num_orgao = {
        'Unidades':0,
        'endereço':0,
        'telefone':0,
        'horário_atendimento':0,
        'competência':0
    }
def search_pages(object, keyword):
    #Not working yet
    return
#--------------------------------------------------------Estrutura Organizacional--------------------------------------------------------
def explain_estrutura_organizacional():
    if(est_org_dict['title'] is not None):
        if (constant.URL not in est_org_dict['url']): url = constant.URL + est_org_dict['url']
        print("Na home do portal foi encontrado um link com o seguinte valor textual:", est_org_dict['title'])
        print("O link", url, "é válido")
    else: 
        print("Não foi encontrada nenhuma das seguintes palavras chave com links validos:")
        for w in constant.ORGANIZACAO:
            print(w)

def search_keywords_estrutura_organizacional(markup, constants):
    for elem in markup.find_all(href=True):
        for s in constants: 
            if s in elem.getText(): 
                est_org_dict['title'] = s
                est_org_dict['url'] = elem['href']
                return True
    return False
       
def predict_estrutura_organizacional():
    #link_list,score = search_pages(object, keyword) #Not working yet
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )

    return search_keywords_estrutura_organizacional(html, constant.ORGANIZACAO)

#--------------------------------------------------------Link Legislação Municipal--------------------------------------------------------
def explain_link_legislacao():
    if(link_legislacao_dict['title']):
        if (constant.URL not in link_legislacao_dict['url']): url = constant.URL + link_legislacao_dict['url']
        print("Na home do portal foi encontrado um link com o seguinte valor textual:", link_legislacao_dict['title'])
        print("O link", url, "é válido")
    else: 
        print("Não foi encontrada nenhuma das seguintes palavras chave com links validos:")
        for w in constant.LEGISLACAO_MUNICIPAL:
            print(w)

def search_keywords_link_legislacao(markup, search):

    for elem in markup.find_all(href=True):
        for s in search: 
            if s in elem.getText(): 
                link_legislacao_dict['title'] = s
                link_legislacao_dict['url'] = elem['href']
                return True
    return False
       
def predict_link_legislacao():
    #link_list,score = search_pages(object, keyword) #Not working yet
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )
    return search_keywords_link_legislacao(html, constant.LEGISLACAO_MUNICIPAL)
#--------------------------------------------------------Unidades Administrativas--------------------------------------------------------
def explain_unidades_administrativas():
    print("A porcentagem de requisitos atendidos para cada categoria foi: ", checklist_info_institucionais_percent,
    "\nPara valores maiores que 60% o item foi considerado como atendido.")
    
def count_orgao(Unidades,Endereco_Telefone,Horario,Competencia):
    min_lengh = 5 
    if len(Unidades.getText()) > min_lengh:
        num_orgao['Unidades'] = num_orgao['Unidades'] + 1
    if len(Endereco_Telefone.getText()) > min_lengh:
        num_orgao['endereço'] = num_orgao['endereço'] + 1
    if len(Endereco_Telefone.getText()) > min_lengh and "Telefone" in Endereco_Telefone.getText():
        num_orgao['telefone'] = num_orgao['telefone'] + 1
    if Horario is not None:
        if len(Horario.getText()) > min_lengh:
            num_orgao['horário_atendimento'] = num_orgao['horário_atendimento'] + 1
    if Competencia is not None:
        if len(Competencia.getText()) > min_lengh:
            num_orgao['competência'] = num_orgao['competência'] + 1

def get_children_classes(elem):
    Unidades = elem.find(class_="nmUnidade")
    Endereco_Telefone = elem.find(class_="dsEndereco well")
    Horario = elem.find(class_="dsHorarioFuncionamento well")
    Competencia = elem.find(class_="dsCompetencias well")
    count_orgao(Unidades,Endereco_Telefone,Horario,Competencia)

def get_values():
    for key in checklist_info_institucionais_percent:
        checklist_info_institucionais_percent[key] = round(num_orgao[key]/num_orgao['Unidades'],2)
        if checklist_info_institucionais_percent[key] > 0.6:
            checklist_info_institucionais[key] = True
    
    return checklist_info_institucionais

def predict_unidades_administrativas():
    #link_list,score = search_pages(object, keyword) #Not working yet
    file = codecs.open('Governador Valadares/organograma/organograma.html', 'r', 'utf-8')
    html = BeautifulSoup(file.read(), "html.parser")
    for elem in html.find_all(class_="divDadosUnidade"):
        get_children_classes(elem)
    values = get_values()
    return values


