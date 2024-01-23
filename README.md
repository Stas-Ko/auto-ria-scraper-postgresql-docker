# auto-ria-scraper-postgresql-docker

Бизнес задача

Обязательно:
Нужно создать программу для периодического скрапинга платформы AutoRia, а именно б/у авто (ссылка на стартовую страницу которую можно внести хардкодом).

Программа должна запускаться каждый день в 00:00 и проходить по всем страницам начиная со стартовой страницы и до конца, заходя в каждую карточку авто и выполнять сбор данных.

Все данные должны сохраняться в базе данных - PostgreSQL.

Программа должна выполнять ежедневный дамп базы данных в 00:00 и хранить файлы дампа в папке “dumps”, которая должна находится рядом с программой.

Готовое тестовое отправить в формате ссылки на Git репозиторий.

Дополнительно: 
Программа и база данных разворачиваются с помощью docker-compose.

Поля базы данных:
- url (строка);
- title (строка);
- price_usd (число);
- odometer (число, нужно перевести 95 тыс. в 95000 и записать как число);
username (строка);
phone_number (число, пример структуры: +38063……..);
image_url (строка);
images_count (число);
car_number (строка);
car_vin (строка);
datetime_found (дата сохранения в базу);





# Автоматизированный сбор данных о продаже автомобилей

Этот проект представляет собой набор скриптов для автоматизации сбора и обработки информации о продаже автомобилей с веб-сайта.

## Структура проекта

- `main.py`: Основной скрипт, который запускает весь процесс.
- `ad_info_collector.py`: Скрипт для сбора информации с объявлений.
- `phone_number_handler.py`: Скрипт для обработки номеров телефонов.
- `db_insert_script.py`: Скрипт для вставки данных в базу данных.
- `time_task_man.py`: Планировщик задач для установки времени запуска скрипта и создания дампа базы данных.

## Использование

1. Запустите `main.py` для начала сбора данных.
2. `ad_info_collector.py` собирает информацию с объявлений.
3. `phone_number_handler.py` обрабатывает номера телефонов.
4. `db_insert_script.py` вставляет данные в базу данных.
5. `time_task_man.py` настраивает планировщик задач.

## Требования к окружению

Установите необходимые библиотеки с использованием команды:

```bash
pip install -r requirements.txt



