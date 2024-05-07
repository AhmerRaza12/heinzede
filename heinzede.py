from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import requests
import os
import pandas
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException


Options = webdriver.ChromeOptions()
Options.add_argument('--no-sandbox')
Options.add_argument('--disable-dev-shm-usage')
Options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
Options.add_argument('--start-maximized')
Options.add_argument('--disable-gpu')
Options.add_argument('--disable-extensions')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=Options)
email = 'kontakt@neu-west.com'
password = 'bepytex2pys' 

def login_site():
    driver.get('https://ausschreibungstexte.heinze.de/')
    time.sleep(5)
    try:
        cookie_buttons=driver.find_element(By.XPATH,"//a[contains(.,'Accept all')]")
        cookie_buttons.click()
        time.sleep(5)
        email_input = driver.find_element(By.XPATH,"//div[@id='loginform-1115-innerCt']/div[2]/div/div/div/input")
       
        for char in email:
            email_input.send_keys(char)
            time.sleep(0.5)
        password_input = driver.find_element(By.XPATH,"//div[@id='loginform-1115-innerCt']/div[3]/div/div/div/input")
        for char in password:
            password_input.send_keys(char)
            time.sleep(0.5)
        time.sleep(2)
        login_button = driver.find_element(By.XPATH,"//a[@data-componentid='form-login-button-signon-1122']")
        login_button.click()
        time.sleep(5)
         # Initially visible tr elements
        first_trs = driver.find_elements(By.XPATH, "//tr[@class='  x-grid-row']/td[@class='x-grid-cell x-grid-td x-grid-cell-colName x-grid-cell-treecolumn x-grid-cell-first x-unselectable']")
        
        # Clicking only the first tr element
        if len(first_trs) >= 1:
            first_trs[0].click()
            time.sleep(2)  
        
            while True:
                # Scroll to load more content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
              
                # New tr elements after scrolling
                new_trs = driver.find_elements(By.XPATH, "//tr[@class='  x-grid-row']/td[@class='x-grid-cell x-grid-td x-grid-cell-colName x-grid-cell-treecolumn x-grid-cell-first x-unselectable']")
                
                # Filter out tr elements that were already clicked
                new_trs = [tr for tr in new_trs if tr not in first_trs]
                
                # Clicking on the new tr elements
                for tr in new_trs:
                    tr.click()
                    time.sleep(2)
                
                # Update the first_trs list with the newly clicked tr elements
                first_trs.extend(new_trs)
                
                # Break the loop if no new tr elements are found
                if not new_trs:
                    break
            
    except Exception as e:
        print(e)
       




if __name__ == '__main__':
    login_site()