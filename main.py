import requests
from bs4 import BeautifulSoup
from ad_info_collector import get_current_page_info
from db_insert_script import insert_data
import logging


# Настройки логирования
logging.basicConfig(filename='main_script.log', level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def start_main_fun():
    url = 'https://auto.ria.com/uk/car/used/'

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок при запросе

            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')

            # Найдем все элементы <section> с классом "ticket-item"
            ticket_sections = soup.find_all('section', class_='ticket-item')

            # Проходим по каждому элементу <section> и извлекаем ссылку из <a class="m-link-ticket">
            for ticket_section in ticket_sections:
                link_element = ticket_section.find('a', class_='m-link-ticket')
                if link_element:
                    link_url = link_element.get('href')
                    try:

                        insert_data(*get_current_page_info(link_url))

                    except Exception as e:
                        # Логируем исключение
                        logging.error(f"Произошла ошибка при обработке ссылки {link_url}: {e}", exc_info=True)

            prefetch_link = soup.find('link', rel='prefetch')
            if prefetch_link:
                url = prefetch_link.get('href')

        except requests.RequestException as req_exc:
            # Логируем исключение при запросе
            logging.error(f"Произошла ошибка при запросе {url}: {req_exc}", exc_info=True)
        except Exception as exc:
            # Логируем общие ошибки
            logging.error(f"Произошла неизвестная ошибка: {exc}", exc_info=True)

if __name__ == "__main__":
    start_main_fun()
