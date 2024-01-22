from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
#url = 'https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35861482.html'

def get_number(url):

    # Создаем объект ChromeOptions для настройки браузера
    chrome_options = Options()

    #chrome_options.add_argument('--remote-debugging-address=127.0.0.1')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #chrome_options.add_argument('--headless')

    # Запускаем браузер с настройками
    driver = webdriver.Chrome(options=chrome_options)

    # Открываем указанную страницу

    driver.get(url)

    driver.execute_script("window.scrollBy(0, 400);")

    # Получаем HTML-код страницы
    html = driver.page_source

    # Используем Beautiful Soup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем элементы с классом "phone" внутри блока с id="phonesBlock"
    phone_elements = soup.select('#phonesBlock .phones_item .phone')

    # Находим первый элемент
    #first_phone_element = driver.find_element(By.CSS_SELECTOR, '#phonesBlock .phones_item .phone')

    # Находим первый элемент
    first_phone_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#phonesBlock .phones_item .phone'))
    )

    # Выполняем двойной клик на элементе
    ActionChains(driver).double_click(first_phone_element).perform()
    time.sleep(1)

    #contains_letters_and_digits = any(char.isalpha() for char in phones_items.text) and any(
        #char.isdigit() for char in phones_items.text)

    #phones_items = driver.find_element('class name', 'phones_item')

        # Используем явное ожидание для поиска элемента phones_item
        #phones_items = EC.presence_of_element_located((By.CLASS_NAME, 'phones_item'))
        #phones_items = driver.find_elements(By.CLASS_NAME, 'phones_item')
    #phones_items = driver.find_element('class name', 'phones_item')

    # Используем явное ожидание для поиска элемента phones_item
    phones_items = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'phones_item'))
    )

    #print(phones_items.text[0:15])

        #contains_letters_and_digits = any(char.isalpha() for char in phones_items.text) and any(
            #char.isdigit() for char in phones_items.text)

        #print(contains_letters_and_digits)

    cleaned_phone_number = ''.join(filter(str.isdigit, phones_items.text[0:15]))
    formatted_phone_number = '+38' + cleaned_phone_number
    #print(int(formatted_phone_number))

    #print(int(phones_items.text[0:15]))

    # Закрываем браузер после использования
    driver.quit()

    return formatted_phone_number
