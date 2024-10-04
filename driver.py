from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    # Настройки для Chrome
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    options =webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random_user_agent}")

    driver = webdriver.Chrome(options=options)


    return driver