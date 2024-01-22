import requests
from bs4 import BeautifulSoup
import re
from phone_number_handler import get_number

def get_current_page_info(url):
    try:
        # Отправляем GET-запрос на текущую страницу
        response = requests.get(url)  # Замените на ваш URL

        # Проверяем успешность запроса
        response.raise_for_status()

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем элементы, как и в вашем оригинальном коде
        heading_div = soup.find('div', class_='heading')
        h1_element = heading_div.find('h1', class_='head', title=True)

        price_div = soup.find('div', class_='price_value')
        strong_element = price_div.find('strong', class_='')

        size18_element = soup.find('span', class_='size18')

        seller_name_div = soup.find('div', class_='seller_info_name bold')

        #phone_number_span = soup.find('span', class_='mhide')

        if h1_element:
            title_content = h1_element['title']
            print(f"Title content: {title_content}")

        if strong_element:
            price_usd = strong_element.get_text(strip=True)
            price_usd = ''.join(filter(str.isdigit, price_usd))
            price_usd = int(price_usd) if price_usd else 0
            print(f"Price in USD: {price_usd}")
        else:
            print("No price element found.")

        if size18_element:
            odometer = size18_element.get_text(strip=True)
            print(f"Odometer: {odometer}")
        else:
            print("No size18 element found.")

        if seller_name_div:
            username = seller_name_div.get_text(strip=True)
            print(f"Username: {username}")
        else:
            # Если не найден seller_info_name, ищем h4 с классом seller_info_name
            alt_seller_name_h4 = soup.find('h4', class_='seller_info_name')

            if alt_seller_name_h4:
                #alt_username = alt_seller_name_h4.get_text(strip=True)
                username = alt_seller_name_h4.get_text(strip=True)
                #print(f"Username: {alt_username}")
                print(f"Username: {username}")
            else:
                print("-")

        #if phone_number_span:
            #phone_number = phone_number_span.get_text(strip=True)
            #print(f"Phone number: {phone_number}")
        #else:
            #print("No mhide element found.")

        print(f"Phone number: {get_number(url)}")

        # Добавляем код для поиска изображения
        div_tag = soup.find('div', class_='gallery-order carousel')

        if div_tag:
            img_tag = div_tag.find('img')

            if img_tag:
                image_url = img_tag['src']
                print(f"Image URL: {image_url}")
            else:
                print("No <img> tag found inside <div class='gallery-order carousel'>.")

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
                        print(f"Images count: {images_count}")
                    else:
                        print("No numbers found in the text.")
                else:
                    print("No <a> tag found inside <div class='action_disp_all_block'>.")
            else:
                images_count = "-"
                print("-")

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
                    print(f"Car VIN: {car_vin}")
                else:
                    car_vin = "-"
                    print("-")  # Выводим прочерк, если нет <span class='label-vin'> tag
            else:
                car_vin = "-"
                print("-")  # Выводим прочерк, если нет <span class='label-vin'> tag
        else:
            car_vin = "-"
            print("No <div class='gallery-order carousel'> tag found.")

        # Находим элемент с классом "state-num ua"
        car_number_span = soup.find('span', class_='state-num ua')

        if car_number_span:
            # Получаем содержимое тега <span class="state-num ua">
            car_number_content = car_number_span.get_text(strip=True)[0:10]
            print(f"Car Number: {car_number_content}")
        else:
            car_number_content = "-"
            print("-")  # Выводим прочерк, если нет <span class='state-num ua'> tag

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")


    return url, title_content, price_usd, odometer, username, get_number(url), image_url, images_count, car_number_content, car_vin

if __name__ == "__main__":
    get_current_page_info('https://auto.ria.com/uk/auto_honda_cr_v_35885178.html')
