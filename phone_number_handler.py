import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

# Настройки логирования
logging.basicConfig(filename='get_number.log', level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_number(url):
    try:
        # Создаем объект ChromeOptions для настройки браузера
        chrome_options = Options()

        # chrome_options.add_argument('--remote-debugging-address=127.0.0.1')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Включает браузер в фоновом режими
        # chrome_options.add_argument('--headless')

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
        first_phone_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#phonesBlock .phones_item .phone'))
        )

        # Выполняем двойной клик на элементе
        ActionChains(driver).double_click(first_phone_element).perform()
        time.sleep(1)

        # Используем явное ожидание для поиска элемента phones_item
        phones_items = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'phones_item'))
        )

        cleaned_phone_number = ''.join(filter(str.isdigit, phones_items.text[0:15]))
        formatted_phone_number = '+38' + cleaned_phone_number

        # Закрываем браузер после использования
        driver.quit()

        return formatted_phone_number

    except Exception as e:
        logging.error(f"Error in get_number: {e}", exc_info=True)
        return None  # Возвращаем None в случае ошибки

if __name__ == "__main__":
    url = 'https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35861482.html'
    result = get_number(url)
    if result:
        print(f"Formatted phone number: {result}")
    else:
        print("Failed to retrieve phone number. Check the logs for details.")
