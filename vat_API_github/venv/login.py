import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 


class Browser: 
    browser, service = None, None

    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)
       
    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(4)

    def login_vat(self, username: str, password: str):
        self.add_input(by=By.ID, value='username', text=username)
        self.add_input(by=By.ID, value='password', text=password)
        self.click_button(by=By.ID, value='login')
        time.sleep(2)
        code = input("Enter duo code: ")
        time.sleep(2)
        self.add_input(by=By.ID, value='o', text=code)
        self.click_button(by=By.ID, value='login')
        time.sleep(1) # click accept terms
        element = self.browser.find_element(By.ID,'accept')
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        self.click_button(by=By.ID, value='accept')

    def get_cookies(self):
        return self.browser.get_cookies()


def login():
    browser = Browser('drivers/chromedriver')
    browser.open_page('https://randomLoginPage')
    time.sleep(2)

    load_dotenv()
    browser.login_vat(os.getenv("USERNAME"), os.getenv("PASSWORD"))

    time.sleep(5)

    cookies = browser.get_cookies()

    for cookie in cookies:
        print(f"Name: {cookie['name']}, Value: {cookie['value']}")

    browser.close_browser()

    return cookies