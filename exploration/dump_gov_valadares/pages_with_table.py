# +
import os
from time import sleep

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException


# -

def get_page_source(driver, path, folder, page, timeout=10, verbose=False):
    
    if verbose:
        print("Get page source")
    
    try:
        element = EC.presence_of_element_located((By.ID, 'datatable_processing'))
        WebDriverWait(driver, timeout).until(element)
        html_source = driver.page_source

        with open('{}/{}/{}_{}.html'.format(path,folder,folder,page), 'w') as f:
            f.write(html_source)
    except TimeoutException:
        print ("Timed out")


def cookie_consent(driver, timeout=10, verbose=False):
    
    if verbose:
        print("Cookie Consent")
    
    try:
        element = EC.presence_of_element_located((By.ID, 'cookieConsent'))
        WebDriverWait(driver, timeout).until(element)
        driver.find_element_by_xpath('//*[@id="closeCookieConsent"]').click()
    except ElementNotInteractableException:
        pass
    except ElementClickInterceptedException:
        pass


def click_next_page(driver, page, timeout=10, verbose=False):
    
    if verbose:
        print("Next page")
    
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "datatable_paginate")))
        next_page = element.find_element_by_class_name("pagination").find_element_by_link_text(str(page))
        next_page.click()
            
        page+=1
        
    except NoSuchElementException:
        pass
    except StaleElementReferenceException:
        pass
    except ElementClickInterceptedException:
        pass
    
    return page


def get_pages_with_table(driver, folder, path, number_pages, timeout=5, verbose=False):

    page = 1

    while (True):
        
        if verbose:
            print("Page: {}".format(page))

        get_page_source(driver, path, folder, page, timeout=10)
        cookie_consent(driver, timeout=10)
        page = click_next_page(driver, page, timeout)
        
        if page == number_pages:
            break
        
    if verbose:
        print("Number of pages: {}".format(page))


def main_pages_with_table(url, path, folder, number_pages, timeout=30, verbose=True):
    
    driver = webdriver.Firefox()
    driver.get(url)
    
    try:
        os.mkdir('{}/{}'.format(path, folder))
    except OSError as error:
        print(error)    
        
    get_pages_with_table(driver, folder, path, number_pages=number_pages, timeout=timeout, verbose=verbose)
    
    driver.quit()


# +
folder = 'receitas-por-dias'
url = 'https://transparencia.valadares.mg.gov.br/receitas-por-dias'
path = '../../../persistence_area/gv'
number_pages=539
timeout=10

main_pages_with_table(url, path, folder, number_pages=number_pages, timeout=timeout, verbose=True)
