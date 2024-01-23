import schedule
import time
from db_insert_script import create_database_dump
from main import start_main_fun

def db_dump():
    # Функция для выполнения дампа базы данных
    create_database_dump()
    
def main_fun():
    # Запуск основной функции 
    start_main_fun()
    
def schedule_jobs():
    # Установка расписания для каждой функции
    schedule.every().day.at("13:08").do(db_dump)
    schedule.every().day.at("13:08").do(main_fun)

    
if __name__ == "__main__":
    # Установка расписания для выполнения функций по времени
    schedule_jobs()

    while True:
        # Цикл для выполнения отложенных задач
        schedule.run_pending()
        time.sleep(1)

