from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
timeout = 5
driver = webdriver.Chrome("/usr/bin/chromedriver")


url_faq = "https://transparencia.valadares.mg.gov.br/perguntas-frequentes"
url_acess = "https://transparencia.valadares.mg.gov.br/acessibilidade"
url_control = "https://transparencia.valadares.mg.gov.br/detalhe-da-unidade/nome/controladoria-geral-do-municipio/14"
url_acesso_informacao = "https://transparencia.valadares.mg.gov.br/servico-de-informacao-ao-cidadao"
url_parcerias = "https://transparencia.valadares.mg.gov.br/parceria-com-osc"
url_home = "https://transparencia.valadares.mg.gov.br/principal"

def accept_cookies():
    try:
        # element = EC.presence_of_element_located((By.ID, 'cookieConsent'))
        element = EC.element_to_be_clickable((By.ID, 'cookieConsent'))
        WebDriverWait(driver, timeout).until(element)
        driver.find_element_by_xpath('//*[@id="closeCookieConsent"]').click()
        print("Cookies Accept")
        time.sleep(2)
    except:
        driver.quit()


def write_file(name, content):
    with open(name, 'w') as arq:
        arq.write(content)
        arq.close()


def main():

    # Perguntas Frequentes
    driver.get(url_faq)
    time.sleep(1)
    accept_cookies()
    
    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("perguntas_frequentes.html",allhtml)

    time.sleep(1)

    alltext =  driver.find_element_by_tag_name('html').text
    write_file("perguntas_frequentes.txt",alltext)

    time.sleep(1)
    # driver.close()


    # Acessibilidade
    driver.get(url_acess)
    time.sleep(2)
    
    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("acessibilidade.html",allhtml)
    alltext =  driver.find_element_by_tag_name('html').text
    write_file("acessibilidade.txt",alltext)

    #Controladoria
    time.sleep(1)
    driver.get(url_control)
    time.sleep(5)
    
    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("controladoria.html",allhtml)
    alltext =  driver.find_element_by_tag_name('html').text
    html_text = BeautifulSoup(allhtml, "html5lib").get_text()
    write_file("bs4_controladoria.txt",html_text)

    # Acesso Informação
    time.sleep(1)
    driver.get(url_acesso_informacao)
    time.sleep(5)

    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("acesso_informacao.html",allhtml)
    alltext =  driver.find_element_by_tag_name('html').text
    html_text = BeautifulSoup(allhtml, "html5lib").get_text()
    write_file("bs4_acesso_informacao.txt",html_text)

    # Relatório Solicitação de informações
    driver.find_element_by_xpath('//*[@id="btn_gerarRelatorio"]').click()
    time.sleep(2)


    # Parcerias
    driver.get(url_parcerias)
    time.sleep(2)
    
    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("parcerias.html",allhtml)
    time.sleep(1)
    alltext =  driver.find_element_by_tag_name('html').text
    write_file("parcerias.txt",alltext)

    # Home
    driver.get(url_home)
    time.sleep(2)
    
    allhtml = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    write_file("home.html",allhtml)
    time.sleep(1)
    alltext =  driver.find_element_by_tag_name('html').text
    write_file("home.txt",alltext)

    time.sleep(2)
    

    driver.quit()



main()