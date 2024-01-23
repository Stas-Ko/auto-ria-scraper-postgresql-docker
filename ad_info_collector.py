import requests
from bs4 import BeautifulSoup
import re
from phone_number_handler import get_number
import logging

# Настройки логирования
logging.basicConfig(filename='get_current_page_info.log', level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_current_page_info(url):
    try:
        # Отправляем GET-запрос на текущую страницу
        response = requests.get(url)
        response.raise_for_status()  # Проверка наличия ошибок при запросе

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим элементы, как и в вашем оригинальном коде
        heading_div = soup.find('div', class_='heading')
        h1_element = heading_div.find('h1', class_='head', title=True)

        price_div = soup.find('div', class_='price_value')
        strong_element = price_div.find('strong', class_='')

        size18_element = soup.find('span', class_='size18')

        seller_name_div = soup.find('div', class_='seller_info_name bold')

        if h1_element:
            title_content = h1_element['title']
            logging.info(f"Title content: {title_content}")

        if strong_element:
            price_usd = strong_element.get_text(strip=True)
            price_usd = ''.join(filter(str.isdigit, price_usd))
            price_usd = int(price_usd) if price_usd else 0
            logging.info(f"Price in USD: {price_usd}")
        else:
            logging.warning("No price element found.")

        if size18_element:
            odometer = size18_element.get_text(strip=True)
            logging.info(f"Odometer: {odometer}")
        else:
            logging.warning("No size18 element found.")

        if seller_name_div:
            username = seller_name_div.get_text(strip=True)
            logging.info(f"Username: {username}")
        else:
            # Если не найден seller_info_name, ищем h4 с классом seller_info_name
            alt_seller_name_h4 = soup.find('h4', class_='seller_info_name')

            if alt_seller_name_h4:
                username = alt_seller_name_h4.get_text(strip=True)
                logging.info(f"Username: {username}")
            else:
                logging.warning("No seller name found.")

        #logging.info(f"Phone number: {get_number(url)}")

        # Добавляем код для поиска изображения
        div_tag = soup.find('div', class_='gallery-order carousel')

        if div_tag:
            img_tag = div_tag.find('img')

            if img_tag:
                image_url = img_tag['src']
                logging.info(f"Image URL: {image_url}")
            else:
                image_url = '-'
                logging.warning("No <img> tag found inside <div class='gallery-order carousel'>.")

            # Находим элемент с классом "action_disp_all_block"
            action_disp_all_block = soup.find('div', class_='action_disp_all_block')

            if action_disp_all_block:
                # Находим тег <a> внутри action_disp_all_block
                show_all_link = action_disp_all_block.find('a')

                if show_all_link:
                    # Получаем содержимое ссылки
                    images_count_data = show_all_link.get_text(strip=True)

                    # Используем регулярное выражение для извлечения чисел
                    numbers = re.findall(r'\d+', images_count_data)

                    if numbers:
                        # Преобразуем найденные числа в формат int и выводим
                        images_count = int(numbers[0])
                        logging.info(f"Images count: {images_count}")
                    else:
                        images_count = '-'
                        logging.warning("No numbers found in the text.")
                else:
                    images_count = '-'
                    logging.warning("No <a> tag found inside <div class='action_disp_all_block'>.")
            else:
                images_count = '-'
                logging.warning("No <div class='action_disp_all_block'> tag found.")

            # Находим элемент с классом "label-vin"
            label_vin_span = soup.find('span', class_='label-vin')

            if label_vin_span:
                # Получаем содержимое тега <span class="label-vin">
                vin_content = label_vin_span.get_text(strip=True)

                # Используем регулярное выражение для извлечения VIN-номера
                vin_numbers = re.search(r'\b([A-HJ-NPR-Z0-9]{17})\b', vin_content)

                if vin_numbers:
                    # Выводим VIN-номер
                    car_vin = vin_numbers.group(0)
                    logging.info(f"Car VIN: {car_vin}")
                else:
                    car_vin = '-'
                    logging.warning("No VIN number found.")
            else:
                car_vin = '-'
                logging.warning("No <span class='label-vin'> tag found.")
        else:
            car_vin = '-'
            logging.warning("No <div class='gallery-order carousel'> tag found.")

        # Находим элемент с классом "state-num ua"
        car_number_span = soup.find('span', class_='state-num ua')

        if car_number_span:
            # Получаем содержимое тега <span class="state-num ua">
            car_number_content = car_number_span.get_text(strip=True)[:10]
            logging.info(f"Car Number: {car_number_content}")
        else:
            car_number_content = '-'
            logging.warning("No <span class='state-num ua'> tag found.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during request: {e}")

    return url, title_content, price_usd, odometer, username, get_number(url), image_url, images_count, car_number_content, car_vin

if __name__ == "__main__":
    get_current_page_info('https://auto.ria.com/uk/auto_land_rover_range_rover_35913460.html#prevAuto=35855950')
