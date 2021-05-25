#Script that iterates through each page and renders all ajax and js elements. Then the DOM for each page is downloaded in an HTML file.
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep

PATH = "C:\Program Files (x86)\geckodriver.exe"
driver = webdriver.Firefox(executable_path = PATH)


#Funciona para Contas Públicas, Estagiários e Concursos Públicos
url_contas = "https://transparencia.valadares.mg.gov.br/contas-publicas"

directory = 'Governador Valadares/contas-publicas/'
url = url_contas


def accept_cookies():
    try:
        # element = EC.presence_of_element_located((By.ID, 'cookieConsent'))
        element = EC.element_to_be_clickable((By.ID, 'cookieConsent'))
        WebDriverWait(driver, 5).until(element)
        driver.find_element_by_xpath('//*[@id="closeCookieConsent"]').click()
        print("Cookies Accept")
        sleep(2)
    except:
        driver.quit()

#Function that gets all rendered DOM and downloads it
def download_file(page_number):
    html = driver.find_element_by_id('lista_resultados').get_attribute('innerHTML')
    filename = directory + str(page_number) + '.html'
    with open(filename,'w',encoding = 'utf-8') as f:
        f.write(html)

#Goes to next page
def get_new_list(nav, page_number):
    if (page_number - 1) % 10 != 0: 
        next_page_btn = nav.find_element_by_link_text(str(page_number))
    else:
        next_page_btn = nav.find_element_by_link_text('»')

    next_page_btn.send_keys(Keys.RETURN) 

#Checks if were rendering and downloading each page
class check_page(object): 
    def __init__(self, nav, page_number):
        self.nav = nav
        self.page_number = page_number

    def __call__(self, driver):
        btn = self.nav.find_element_by_class_name('active').find_element_by_tag_name('a')
        if btn.text == str(self.page_number):
            return btn
        else: return False

def main ():    
    driver.get(url)
    accept_cookies()
    page_number = 1
    number_of_pages = math.ceil(int(driver.find_element_by_id('lbl_TotalRegistros').text)/10)
    try: 
        while(True):
            print('Verificando se estamos na página: ', page_number)            
            nav = driver.find_element_by_class_name('pagination-content')             
            element = WebDriverWait(driver, 10).until(check_page(nav, page_number))
            sleep(2)
            download_file(page_number)
            page_number += 1
            if(page_number >= number_of_pages): 
                break
            print('Navegando para a página: ', page_number)
            get_new_list(nav, page_number)

    
    finally:
        driver.quit()

main()