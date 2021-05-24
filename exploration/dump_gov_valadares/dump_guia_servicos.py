#Script that iterates through each page and renders all ajax and js elements. Then the html elements that contain files
#in each page are downloaded.

import math
from os import close

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

PATH = "C:\Program Files (x86)\geckodriver.exe"
driver = webdriver.Firefox(executable_path = PATH)

url = 'https://transparencia.valadares.mg.gov.br/servicos'   


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
def download_file(page_number, html):
    try: 
        print('Downloading page ', page_number)
        dir = 'Governador Valadares/servicos/'
        with open(dir + str(page_number) + '.html','w',encoding = 'utf-8') as f:
            f.write(html)
        sleep(1)
    except (NoSuchElementException, StaleElementReferenceException) :
        print('Couldnt download page ', page_number)


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

#Goes to next page
def get_new_list(nav, page_number):
    if (page_number - 1) % 10 != 0: 
        next_page_btn = nav.find_element_by_link_text(str(page_number))
    else:
        next_page_btn = nav.find_element_by_link_text('»')

    next_page_btn.send_keys(Keys.RETURN) 

#Clicks in each element downloading its content
def process_page(page_number):
    
    list_of_btns = driver.find_element_by_id('listagem').find_elements_by_tag_name('a')    
    html = ''
    
    for btn in list_of_btns:
        html += '<div class="servico"> ' 
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "listagem")))        
        html += btn.get_attribute('innerHTML')
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
    
    download_file(page_number, html)
        

def main ():    
    driver.get(url)
    accept_cookies()
    number_of_pages = math.ceil(int(driver.find_element_by_id('lbl_TotalRegistros').text)/10)    
    page_number = 1

    
    try: 
        while(True):
            nav = driver.find_element_by_class_name('pagination-content')             
            WebDriverWait(driver, 10).until(check_page(nav, page_number))
            process_page(page_number)
            page_number += 1
            if(page_number > number_of_pages): break
            get_new_list(nav, page_number)  
            
    except (NoSuchElementException, StaleElementReferenceException):
        print('Couldnt open page')
    
    finally: 
        driver.quit()

main()

