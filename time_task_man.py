import threading
import schedule
from db_insert_script import create_database_dump
from main import start_main_fun

def db_dump():
    # Функция для выполнения дампа базы данных
    create_database_dump()
    print('Database dump completed')

def main_fun():
    # Основная функция, которую вы хотите запустить
    start_main_fun()
    print('Main function completed')

def run_scheduled_jobs():
    # Цикл для выполнения отложенных задач
    while True:
        schedule.run_pending()

def schedule_jobs():
    # Установка расписания для каждой функции
    schedule.every().day.at("00:00").do(db_dump)
    schedule.every().day.at("00:00").do(main_fun)

if __name__ == "__main__":
    # Создание двух потоков для выполнения функций параллельно
    db_dump_thread = threading.Thread(target=db_dump)
    main_fun_thread = threading.Thread(target=main_fun)

    # Запуск потоков
    db_dump_thread.start()
    main_fun_thread.start()

    # Запуск цикла для выполнения отложенных задач
    run_scheduled_jobs()

    # Ожидание завершения потоков
    db_dump_thread.join()
    main_fun_thread.join()
