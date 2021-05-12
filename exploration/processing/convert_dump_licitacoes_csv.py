from bs4 import BeautifulSoup
import pandas as pd
import codecs
from os import walk

def extract_data_from_file(id_text):
    el = []
    with codecs.open('dump_gov_valadares_licitacoes.html', 'r', 'utf-8') as file:
        html= BeautifulSoup(file.read())
        for div in html.find_all(id = id_text):
            text = div.getText().split(':', 1)
            print(div.getText())
            print(text)
            el.append(text[1].replace('\n', ''))
    while len(el) < 20:
        el.append('')
    return el

def main():
    new_df = pd.DataFrame({'Ano': extract_data_from_file( 'nuLicitacao_nuAno'),
                        'Número Processo Administrativo': extract_data_from_file( 'nuProcessoAdm'),
                        'Modalidade da Licitação': extract_data_from_file( 'nmLicitacaoModalidade'),
                        'Fundamentação Legal': extract_data_from_file( 'nmFundamentoLegal'),
                        'Objeto': extract_data_from_file( 'dsObjeto'),
                        'Unidade solicitante': extract_data_from_file( 'nmUnidade'),
                        'Valor estimado': extract_data_from_file( 'nuValorEstimado'),
                        'Data de publicação': extract_data_from_file( 'dtPublicacao'),
                        'Data limite': extract_data_from_file( 'dtLimite'),
                        'Data de abertura': extract_data_from_file( 'dtHabilitacao'),
                        'Horário de abertura': extract_data_from_file( 'horaHabilitacao'),
                        'Status': extract_data_from_file( 'status')})
    
    new_df.to_csv('licitacoes.csv')
    
main()