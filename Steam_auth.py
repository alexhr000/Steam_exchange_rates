from driver import get_driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

def Steam_auth():
    # Инициализируем WebDriver
    driver = get_driver()  # Убедитесь, что chromedriver в PATH или укажите путь к нему

    # Открываем страницу авторизации Steam
    driver.get('https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header')

    # Вводим логин и пароль
    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div._3XCnc4SuTz8V8-jXVwkt_s > div > form > div:nth-child(1) > input')))
    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,  '#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div._3XCnc4SuTz8V8-jXVwkt_s > div > form > div:nth-child(2) > input')))
    
    # Ввод данных пользователя
    load_dotenv()
    username_input.send_keys(os.getenv('STEAM_LOGIN'))  
    password_input.send_keys(os.getenv('STEAM_PASSWORD'))  

    # Нажимаем кнопку "Войти"
    login_button = driver.find_element(By.CSS_SELECTOR, '#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div._3XCnc4SuTz8V8-jXVwkt_s > div > form > div._16fbihk6Bi9CXuksG7_tLt > button')
    login_button.click()

    # Используем WebDriverWait для ожидания успешной авторизации (например, появления определенного элемента)
    try:
        # Ждем, пока на странице появится элемент, который появляется только после успешной авторизации
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'store_nav_search_term'))  # Элемент, появляющийся после входа
        )
        print("Успешно авторизовались!")
    except TimeoutException:
        print("Авторизация не удалась или заняла слишком много времени")


    # Сохранение cookies
    cookies = driver.get_cookies()
    headers = {
        'User-Agent': driver.execute_script("return navigator.userAgent;")
    }

    # Закрываем браузер
    driver.quit()
    return [cookies, headers]