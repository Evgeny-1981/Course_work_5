import psycopg2

from config import config
from src.api import HeadHunterAPI
from src.dbcreate import DBCreate


params_db = config()
db = DBCreate()
print(db)

database_name = "coursework5"  # Имя базы данных

# employers_dict = response.employers_dict  # Словарь компаний
# employers_all_vacancies = response.get_vacancies()  # Список вакансий
# params = config()  # Конфигом достаем параметры
db.create_database(database_name)  # Статик методом создаем базу данных
db.create_tables(database_name)
# conn = DBCreate(database_name, params_db)  # Создаем экземпляр, класса открываем подключение
# DBManager.create_table_employers(conn)  # Создаем таблицу компаний