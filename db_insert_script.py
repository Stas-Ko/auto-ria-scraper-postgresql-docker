import psycopg2
from psycopg2 import sql
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
import os
import logging

# Функция для создания соединения с базой данных
def create_connection():
    # Вставьте свои данные для подключения к PostgreSQL
    return psycopg2.connect(
        host="localhost",  # Хост сервера PostgreSQL
        port="5432",  # Порт PostgreSQL
        user="postgres",  # Имя пользователя PostgreSQL
        password="Kpfaz851mnz",  # Пароль пользователя PostgreSQL
        database="auto_ria"  # Имя базы данных PostgreSQL
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
def insert_data(url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            try:
                # SQL-запрос для вставки данных с использованием date_trunc
                insert_data_query = sql.SQL("""
                INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, date_trunc('second', current_timestamp))
                """)
                # Значения для вставки
                data_values = (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
                cursor.execute(insert_data_query, data_values)
                connection.commit()
            except psycopg2.Error as e:
                connection.rollback()
                logging.error(f"Error during data insertion: {e}", exc_info=True)

# Функция для создания дампа базы данных
def create_database_dump():
    dump_folder = "dumps"
    os.makedirs(dump_folder, exist_ok=True)
    dump_file = os.path.join(dump_folder, f"dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")

    try:
        with create_connection() as conn, conn.cursor() as cursor:
            with open(dump_file, 'a') as f:  # 'a' - режим добавления данных в файл
                cursor.copy_expert("COPY (SELECT * FROM cars) TO STDOUT WITH CSV", f)
        print(f"Database dump created at {dump_file}")
    except psycopg2.Error as e:
        logging.error(f"Error during database dump creation: {e}", exc_info=True)


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

    # Вызываем функцию для вставки данных в базу
    insert_data(url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)

    # Создаем дамп базы данных
    create_database_dump()
