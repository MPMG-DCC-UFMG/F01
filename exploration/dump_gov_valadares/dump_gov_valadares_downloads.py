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
url = 'https://transparencia.valadares.mg.gov.br/downloads'   


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
def download_file(page_number, category_name):
    try: 
        html = driver.find_element_by_class_name('lista_resultados').get_attribute('innerHTML')
        filename = 'dump_gov_valadares/' + category_name.replace(',', '').replace('.', '').replace('/', '') + '.html'
        with open(filename,'a',encoding = 'utf-8') as f:
            f.write(html)
    except (NoSuchElementException, StaleElementReferenceException) :
        print('Couldnt download ', category_name, ' page number: ', page_number)

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

def download_of_each_category(category_name, number_of_pages):
    page_number = 1
    if number_of_pages <= 1:
            download_file(page_number, category_name)
            return 
    while(True):
        try:
            nav = driver.find_element_by_class_name('pagination-content')   
            WebDriverWait(driver, 5).until(check_page(nav, page_number)) 
            sleep(2)
            download_file(page_number, category_name)
            page_number += 1
            
            if(page_number > number_of_pages): break
            
            #print('Going to page: ', page_number)
            get_new_list(nav, page_number)         
        
        except (NoSuchElementException, StaleElementReferenceException) :
            print('Couldnt download ', category_name, ' page number: ', page_number)
           

def main ():    
    driver.get(url)
    sleep(1)
    accept_cookies()

    list_of_categories = driver.find_element_by_id('categorias').find_element_by_tag_name('ul')
    list_of_categories = list_of_categories.find_elements_by_class_name('nav-header')
    list_of_categories.pop(0)

    try: 
        for category in list_of_categories:
            category_name = unidecode(category.text).replace(' ', '')
            print('Processing: ', category.text)
            
            try:
                category.send_keys(Keys.RETURN) 
                sleep(1)
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id = 'listagem']//h3[1]"), category.text))
                number_of_pages = math.ceil(int(driver.find_element_by_id('lbl_TotalRegistros').text)/10)
                #print('Number of pages: ', number_of_pages)
                download_of_each_category(category_name, number_of_pages)

            
            except NoSuchElementException:
                driver.quit()          
            except (TimeoutException, ElementNotInteractableException) :
                print('Something went very very wrong')
    finally: 
        driver.quit()
main()