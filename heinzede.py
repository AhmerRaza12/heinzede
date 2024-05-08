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
import pandas as pd
import csv
from dotenv import load_dotenv

Options = webdriver.ChromeOptions()
Options.add_argument('--no-sandbox')
Options.add_argument('--disable-dev-shm-usage')
Options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
Options.add_argument('--start-maximized')
# Options.add_argument('--headless=new')


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=Options)
load_dotenv()
email = os.getenv('HEINZEDE_EMAIL')
password = os.getenv('HEINZEDE_PASSWORD')
print(email, password)

def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True


def login_site():
    driver.get('https://ausschreibungstexte.heinze.de/')
    all_data = []
    time.sleep(5)
    try:
        # cookie_buttons= WebDriverWait(driver,10).until(EC.element_to_be_clickable(By.XPATH,"//a[contains(.,'Accept all')]"))
        cookie_buttons = driver.find_element(By.XPATH, "//a[contains(.,'Accept all')]")
        cookie_buttons.click()
        time.sleep(5)

        
        email_input = driver.find_element(By.XPATH, "//div[@id='loginform-1115-innerCt']/div[2]/div/div/div/input")
        for char in email:
            email_input.send_keys(char)
        
        password_input = driver.find_element(By.XPATH, "//div[@id='loginform-1115-innerCt']/div[3]/div/div/div/input")
        for char in password:
            password_input.send_keys(char)
        
        time.sleep(2)
        login_button = driver.find_element(By.XPATH, "//a[@data-componentid='form-login-button-signon-1122']")
        login_button.click()
        time.sleep(5)

        all_trs = driver.find_elements(By.XPATH, "//tr[@class='  x-grid-row']")
        print(len(all_trs))
        
        length = 51
        
        global unique_elements
        for idx in range(0, length):
            first_tr = driver.find_element(By.XPATH, f"//table[@id='boqitems-view-1041-record-{44+idx}']")
            unique_elements = set()
            first_tr.click()

            main_category_element = driver.find_element(By.XPATH, f"//table[@id='boqitems-view-1041-record-{44+idx}']//tr[1]/td/div[1]/span[1]")
            main__text = main_category_element.text
            main_category = main__text.split('(')[0].strip()
            print(main_category)
            time.sleep(1)
            sub_trs = driver.find_elements(By.XPATH, "//tr[@class='  x-grid-row']")
            sub_trs = [tr for tr in sub_trs if tr not in all_trs]
            for new_tr in sub_trs:
                time.sleep(1)
                sub_tr_name_element = new_tr.find_element(By.XPATH, "./td/div[1]/span[1]")
                sub_tr_name_text = sub_tr_name_element.text
                sub_tr_name = sub_tr_name_text.split('(')[0].strip()
                driver.execute_script("arguments[0].scrollIntoView();", new_tr)
                new_tr.click()
                time.sleep(2)
                sub_sub_trs = driver.find_elements(By.XPATH, "//tr[@class='  x-grid-row']")
                sub_sub_trs = [tr for tr in sub_sub_trs if tr not in sub_trs and tr not in all_trs]
                for sub_sub_tr in sub_sub_trs:
                    time.sleep(1)
                    sub_sub_tr_name_element = sub_sub_tr.find_element(By.XPATH, "./td/div[1]/span[1]")
                    sub_sub_tr_name_text = sub_sub_tr_name_element.text
                    sub_sub_tr_name = sub_sub_tr_name_text.split('(')[0].strip()
                    driver.execute_script("arguments[0].scrollIntoView();", sub_sub_tr)
                    sub_sub_tr.click()
                    time.sleep(2)
                    data_trs = driver.find_elements(By.XPATH, "//tr[@class='x-grid-tree-node-leaf  x-grid-row']")
                    for data_tr in data_trs:
                        element_tuple = tuple(data_tr.find_elements(By.XPATH, ".//td/div"))
                        if element_tuple not in unique_elements:
                            unique_elements.add(element_tuple)
                        
                            category = main_category
                            name = data_tr.find_element(By.XPATH, "./td/div[1]/span[1]").text
                            einheit = data_tr.find_element(By.XPATH, "./td[2]/div[1]").text
                            unterer_ep = data_tr.find_element(By.XPATH, "./td[3]/div").text
                            milterer_ep = data_tr.find_element(By.XPATH, "./td[4]/div").text
                            oberer_ep = data_tr.find_element(By.XPATH, "./td[4]/div").text
                            konstengruppe = data_tr.find_element(By.XPATH, "./td[5]/div").text

                            data = {
                                "Category": category,
                                "Sub cat 1": sub_tr_name,
                                "Sub cat 2": sub_sub_tr_name,
                                "Name": name,
                                "Einheit": einheit,
                                "Unterer Ep": unterer_ep,
                                "Milterer_ep": milterer_ep,
                                "Oberer Ep": oberer_ep,
                                "Konsatengrupppe": konstengruppe
                            }
                            # print(data)
                            # success = appendProduct('data.csv', data)
                            # if not success:
                            #     print("Error occurred while appending data to CSV.")  
                            try:
                                
                                with open('data.csv', 'a', newline='', encoding='utf-8') as file:
                                    writer = csv.DictWriter(file, fieldnames=data.keys())
                                    
                                    writer.writerow(data)
                                    
                            except Exception as e:
                                print(f"An error occurred while appending data to CSV: {str(e)}")
                            
                    sub_sub_tr.click()
                    time.sleep(1)
                new_tr.click()
                time.sleep(1)
            first_tr.click()
            time.sleep(1)

    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == '__main__':
    login_site()
    