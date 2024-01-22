import requests
from bs4 import BeautifulSoup
from ad_info_collector import get_current_page_info
from sel_num_phone_fun import get_number
from db_insert_script import insert_data
import logging
import os
from datetime import datetime

# Создаем папку "logs", если ее нет
if not os.path.exists("logs"):
    os.makedirs("logs")

# Определяем имя файла для логирования
log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Настройка логгера
logging.basicConfig(filename=log_file, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Включаем логгирование в консоль
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Пример использования логгера
logging.info("Скрипт запущен")

url = 'https://auto.ria.com/uk/car/used/'

while True:

    response = requests.get(url)
    page_content = response.content

    soup = BeautifulSoup(page_content, 'html.parser')

    # Найдем все элементы <section> с классом "ticket-item"
    ticket_sections = soup.find_all('section', class_='ticket-item')

    # Проходим по каждому элементу <section> и извлекаем ссылку из <a class="m-link-ticket">
    for ticket_section in ticket_sections:
        link_element = ticket_section.find('a', class_='m-link-ticket')
        if link_element:
            link_url = link_element.get('href')
            print(link_url)
            print()
            try:
                #url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin = get_current_page_info(link_url)
                #get_current_page_info(link_url)

                #print(all_data)
                #print(get_number(link_url))
                print('HELLO')

                #insert_data(url, title, price_usd, odometer, username, phone_number, image_url, images_count,
                            #car_number, car_vin)

                insert_data(*get_current_page_info(link_url))

            except Exception as e:
                # Логируем исключение
                logging.error(f"Произошла ошибка: {e}", exc_info=True)

                #print(f"Произошла ошибка: {e}")
  
    prefetch_link = soup.find('link', rel='prefetch')

    if prefetch_link:
        url = prefetch_link.get('href')
        print(url)
    else:
        print("Ссылка с rel='prefetch' не найдена.")
