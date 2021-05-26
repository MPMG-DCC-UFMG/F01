#Script that iterates through each page and renders all ajax and js elements. Then the html elements that contain files
#in each page are downloaded.

import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

PATH = "C:\Program Files (x86)\geckodriver.exe"
driver = webdriver.Firefox(executable_path = PATH)

url = 'https://transparencia.valadares.mg.gov.br/organograma'   
dir = 'Governador Valadares/organograma'

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
def download_file(html):
    try: 
        filename = 'organograma.html'
        with open(dir + '/' + filename,'w',encoding = 'utf-8') as f:
            f.write(html)
    except (NoSuchElementException, StaleElementReferenceException) :
        print('Couldnt download html')

def process_page():
    
    list_of_btns = driver.find_element_by_id('tree').find_elements_by_tag_name('a')    
    html = ''
    
    for btn in list_of_btns:
        html += '<div class="nó lista"> ' 
        try:
            btn.send_keys(Keys.RETURN)
            try:
                sleep(1)
                modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal fade in fv-modal-stack')]"))).find_element_by_class_name('modal-content')
                html += modal.get_attribute('innerHTML')
                close_btn = WebDriverWait(modal, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "close")))
                close_btn.click()
        
            except (NoSuchElementException, StaleElementReferenceException):
                print('Modal wasnt loaded correctly')
            except ElementNotInteractableException:
                print('Couldnt close modal')
        
        except ElementNotInteractableException:
            print('Couldnt open modal')
        
        finally:
            html += '</div>' 
    
    return html

def main ():    
    driver.get(url)
    sleep(1)
    accept_cookies()

    try: 
        open_btn = driver.find_element_by_partial_link_text('Expandir todos')
        
        open_btn.send_keys(Keys.RETURN) 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Recolher todos')))
        
        download_file(process_page())
         
    except (TimeoutException, ElementNotInteractableException, NoSuchElementException) :
        print('Something went very very wrong')
    finally: 
        driver.quit()

main()