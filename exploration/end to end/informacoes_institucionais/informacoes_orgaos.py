import codecs
import os
from bs4 import BeautifulSoup

checklist_info_institucionais = {
    'competência': 0,
    'endereço': 0,
    'telefone': 0,
    'horário_atendimento': 0
}
num_orgao = {
        'Unidades':0,
        'endereço':0,
        'telefone':0,
        'horário_atendimento':0,
        'competência':0
    }
def explain():
    print("O validador procura por todos os Órgãos e retorna a porcentagem de",checklist_info_institucionais.keys(),"presente na URL para cada Órgão.")
    
def count_orgao(Unidades,Endereco_Telefone,Horario,Competencia):
    if len(Unidades.getText()) > 5:
        num_orgao['Unidades'] = num_orgao['Unidades'] + 1
    if len(Endereco_Telefone.getText()) > 5:
        num_orgao['endereço'] = num_orgao['endereço'] + 1
    if len(Endereco_Telefone.getText()) > 5 and "Telefone" in Endereco_Telefone.getText():
        num_orgao['telefone'] = num_orgao['telefone'] + 1
    if Horario is not None:
        if len(Horario.getText()) > 5:
            num_orgao['horário_atendimento'] = num_orgao['horário_atendimento'] + 1
    if Competencia is not None:
        if len(Competencia.getText()) > 5:
            num_orgao['competência'] = num_orgao['competência'] + 1

def get_children_classes(elem):
    checklist_info_institucionais
    Unidades = elem.find(class_="nmUnidade")
    Endereco_Telefone = elem.find(class_="dsEndereco well")
    Horario = elem.find(class_="dsHorarioFuncionamento well")
    Competencia = elem.find(class_="dsCompetencias well")
    count_orgao(Unidades,Endereco_Telefone,Horario,Competencia)

def calculate_percentage():
    for key in checklist_info_institucionais:
        checklist_info_institucionais[key] = num_orgao[key]/num_orgao['Unidades']
    print(checklist_info_institucionais)

def main():
    file = codecs.open('Governador Valadares/organograma/organograma.html', 'r', 'utf-8')
    html = BeautifulSoup(file.read(), "html.parser")
    for elem in html.find_all(class_="divDadosUnidade"):
        get_children_classes(elem)
    explain()
    calculate_percentage()
main()
