from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
timeout = 5
driver = webdriver.Chrome("/usr/bin/chromedriver")

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

def click_listagem():
    try:
        driver.find_element_by_xpath('//*[@id="tbc_item_lista"]').click()
        print("Click Listagem")
    except:
        driver.quit()

def extract_body():
    try:
        element = EC.presence_of_element_located((By.ID, 'cookieConsent'))
        WebDriverWait(driver, timeout).until(element)
        body = driver.find_element_by_xpath('//*[@id="lista"]/div/div')
        return body
    except:
        driver.quit()
        print("body fail")


def main():

    driver.get("https://transparencia.valadares.mg.gov.br/obras")
    time.sleep(1)
    accept_cookies()

    allhtml_map = driver.find_element_by_tag_name('html').get_attribute('innerHTML')

    with open('all_html_map.html', 'w') as all_html_map:
        all_html_map.write(allhtml_map)
        all_html_map.close()


    click_listagem()

    allhtml_list = driver.find_element_by_tag_name('html').get_attribute('innerHTML')

    with open('all_html_list.html', 'w') as all_html_list:
        all_html_list.write(allhtml_list)
        all_html_list.close()

    body = extract_body()
    print(body.get_attribute('innerHTML'))

    with open('obras_txt.txt', 'w') as obras_txt:
        obras_txt.write(body.text)
        obras_txt.close()

    with open('obras_html.html', 'w') as obras_html:
        obras_html.write(body.get_attribute('innerHTML'))
        obras_html.close()


    time.sleep(4)
    driver.quit()


main()