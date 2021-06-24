import codecs
import os
from bs4 import BeautifulSoup

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
def explain():
    print("A porcentagem de requisitos atendidos para cada categoria foi: ", checklist_info_institucionais_percent,
    "\nPara valores maiores que 60% o item foi considerado como atendido.")
    
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
    Unidades = elem.find(class_="nmUnidade")
    Endereco_Telefone = elem.find(class_="dsEndereco well")
    Horario = elem.find(class_="dsHorarioFuncionamento well")
    Competencia = elem.find(class_="dsCompetencias well")
    count_orgao(Unidades,Endereco_Telefone,Horario,Competencia)

def predict():
    for key in checklist_info_institucionais_percent:
        checklist_info_institucionais_percent[key] = round(num_orgao[key]/num_orgao['Unidades'],2)
        if checklist_info_institucionais_percent[key] > 0.6:
            checklist_info_institucionais[key] = True
    
    return checklist_info_institucionais

def main():
    file = codecs.open('Governador Valadares/organograma/organograma.html', 'r', 'utf-8')
    html = BeautifulSoup(file.read(), "html.parser")
    for elem in html.find_all(class_="divDadosUnidade"):
        get_children_classes(elem)
    values = predict()
    explain()
    print(values)

main()
