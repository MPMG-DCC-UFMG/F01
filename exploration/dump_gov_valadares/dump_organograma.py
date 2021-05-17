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
url = 'https://transparencia.valadares.mg.gov.br/organograma'   


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
        html = driver.find_element_by_id('conteudo').get_attribute('innerHTML')
        filename = 'organograma.html'
        with open(filename,'w',encoding = 'utf-8') as f:
            f.write(html)
    except (NoSuchElementException, StaleElementReferenceException) :
        print('Couldnt download html')


def main ():    
    driver.get(url)
    sleep(1)
    accept_cookies()

    try: 
        btn = driver.find_element_by_partial_link_text('Expandir')
        btn.send_keys(Keys.RETURN) 
        sleep(1)
        download_file()
         
    except (TimeoutException, ElementNotInteractableException, NoSuchElementException) :
        print('Something went very very wrong')
    finally: 
        driver.quit()

main()