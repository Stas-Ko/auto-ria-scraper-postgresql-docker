import psycopg2
from psycopg2 import sql
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime

# Функция для создания соединения с базой данных
def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="Kpfaz851mnz",
        database="auto_ria"
    )

# Функция для создания таблицы в базе данных PostgreSQL
def create_table():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            # SQL-запрос для создания таблицы
            create_table_query = """
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255),
                title VARCHAR(255),
                price_usd NUMERIC,
                odometer NUMERIC,
                username VARCHAR(255),
                phone_number NUMERIC,
                image_url VARCHAR(255),
                images_count INTEGER,
                car_number VARCHAR(20),
                car_vin VARCHAR(17),
                datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
        connection.commit()

# Функция для вставки данных в таблицу
# Функция для вставки данных в таблицу
def insert_data(url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            # SQL-запрос для вставки данных с использованием date_trunc
            insert_data_query = sql.SQL("""
            INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, date_trunc('second', current_timestamp))
            """)
            # Значения для вставки
            data_values = (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
            cursor.execute(insert_data_query, data_values)
        connection.commit()

# Ваш существующий код для получения данных
#def get_current_page_info():
    # ... (ваш код для получения данных)

if __name__ == "__main__":
    # Вызываем функцию для создания таблицы (если её нет)
    create_table()

    # Пример данных для базы данных и теста работы
    url = 'https://auto.ria.com/uk/auto_volkswagen_passat_35908049.html'
    title = 'Volkswagen Passat 2018'
    price_usd = 19200
    odometer = 226
    username = 'Славік'
    phone_number = 380993548417
    image_url = 'https://cdn0.riastatic.com/photosnew/auto/photo/volkswagen_passat__533078555f.jpg'
    images_count = 42
    car_number = 'AT 1238 IB'
    car_vin = 'WVWZZZ4CZJP029792'

    #get_current_page_info()
    # Вызываем функцию для вставки данных в базу
    insert_data(url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
