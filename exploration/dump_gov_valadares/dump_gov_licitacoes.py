#Script that iterates through each page and renders all ajax and js elements. Then the html elements that contain files
#in each page are downloaded.

import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait

from unidecode import unidecode
from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH,options=options)
url = 'https://transparencia.valadares.mg.gov.br/licitacoes'   


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
def download_file():
    try: 
        html = driver.find_element_by_id('textos').find_element_by_class_name('list-group').get_attribute('innerHTML')
        filename = 'dump_gov_valadares_licitacoes.html'
        with open(filename,'a',encoding = 'utf-8') as f:
            f.write(html)
        sleep(1)
    except (NoSuchElementException, StaleElementReferenceException) :
        print('Couldnt download data')


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
    try: 
        list_of_btns = driver.find_element_by_id('listagem').find_elements_by_tag_name('a')
        for i in range(len(list_of_btns)):
            sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "listagem")))
            list_of_btns = driver.find_element_by_id('listagem').find_elements_by_tag_name('a')

            list_of_btns[i].send_keys(Keys.RETURN) 
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "lbl_rotuloLocal")))
            print('Download element', i)
            download_file()
            driver.back()
    except ElementNotInteractableException:
        print('Couldnt open page')
    finally: 
        driver.quit()
main()