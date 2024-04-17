import psycopg2

from config import config
from src.api import HeadHunterAPI
from src.dbcreate import DBCreate
from src.dbmanager import DBManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    params_db = config()
    database_name = 'coursework5'

    # создание экземпляра класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # # Предлагаем пользователю ввести город, в котором будет выполнени поиск работодателей, разместивших вакансии
    # # с сохранением информации в словарь с ID работадателя и его названия
    # city_name = input("Введите название города для поиска компаний, разместивших в нем вакансии: ").title()
    # city_id = hh_api.get_city_id(city_name)
    # print(f'Код населенного пункта "{city_name}": {city_id}')

    # # Получаем словарь работодателей, отсортированных по уровню начальной заработной платы
    # employers_dict = hh_api.get_employers(city_id)
    # employer_id_name = {}
    # for employer_id, employer_name in employers_dict.items():
    #     employer_id_name[employer_id] = employer_name['employer_name'], employer_name['employer_url']
    # print(len(employer_id_name))

    #  Получаем список id работодателей из словаря employers_dict
    # employers_list = []
    # for employer in employers_dict:
    #     employers_list.append(employer)

    # #  Запрос количества id работодателей, по которым будет выполнен поиск вакансий
    # num_employer = None
    # while num_employer not in range(1, len(employer_id_name) + 1):
    #     try:
    #         num_employer = int(
    #             input(f'По указанному городу найдено {len(employer_id_name)} компаний, разместивших вакансии.\n'
    #                   f'Введите количество компаний по которым искать вакансии от 0 до {len(employer_id_name)}, '
    #                   f'если ввести "0" и нажать "Enter", то будут выбраны все найденные компании: '))
    #         if num_employer == 0:
    #             num_employer = len(employer_id_name)
    #     except ValueError:
    #         print(f'Ошибка ошибка ввода! Введите целое число от 0 до {len(employer_id_name)}')

    # #  Получаем список словарей словарей вакансий каждого работодателя
    # result_data = []
    # count = 0
    # for employer, name in employer_id_name.items():
    #     if count < num_employer:
    #         vacancies = hh_api.get_vacancies_by_employers(employer, city_id)
    #         result_data.append({'employer': employer, 'name': name[0], 'employer_url': name[1], 'vacancies': vacancies})
    #         count += 1

    # #  Создаем экземпляр класса DBCreate
    # db = DBCreate()
    # print(repr(db))
    # #  Создание базы данных
    # db.create_database(database_name)
    # #  Создание таблиц
    # db.create_tables(database_name)
    # #  Сохранение даных в таблицы
    # db.save_info_to_database(database_name, result_data, city_name)
    db_manager = DBManager
    conn = db_manager(database_name, params_db)
    query_1 = db_manager.get_companies_and_vacancies_count(conn)
    for row in query_1:
        print(f"Компания: '{row[0]}', количество вакансий: {row[1]}")
    query_2 = db_manager.get_all_vacancies(conn)
    for row in query_2:
        print(f"Компания: '{row[0]}', вакансия: '{row[1]}', зарплата: '{row[2]}', URL: '{row[3]}'")
    query_3 = db_manager.get_avg_salary(conn)
    for row in query_3:
        print(f"Средняя зарплата по всем имеющимся вакансиям в базе данных: {round(float(row[0]), 2)} у.е.")
