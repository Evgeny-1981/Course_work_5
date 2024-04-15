import psycopg2
import os
from config import config
from src.api import HeadHunterAPI
from src.dbcreate import DBCreate


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    params_db = config()
    database_name = "coursework5"

    # создание экземпляра класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # Предлагаем пользователю ввести город, в котором будет выполнени поиск работодателей, разместивших вакансии
    # с сохранением информации в словарь с ID работадателя и его названия
    city_name = input("Введите название города для поиска компаний, разместивших в нем вакансии: ").title()
    city_id = hh_api.get_city_id(city_name)
    print(f'Код населенного пункта "{city_name}": {city_id}')

    # Получаем словарь работодателей, отсортированных по уровню начальной заработной платы
    employers_dict = hh_api.get_employers(city_id)
    employer_id_name = {}
    for employer_id, employer_name in employers_dict.items():
        employer_id_name[employer_id] = employer_name['employer_name']
    for i, n in employer_id_name.items():
        print(i,n)
    # Получаем список id работодателей из словаря employers_dict
    employers_list = []
    for employer in employers_dict:
        employers_list.append(employer)
    for i in employers_list:
        print(i)

    # Запрос количества id работодателей, по которым будет выполнен поиск вакансий
    # pause_get = 0  # Пауза при отборе вакансий, если выбрать более 20 работодателей для сбора вакансий
    num_employer = None
    while num_employer not in range(1, len(employers_list) + 1):
        try:
            num_employer = int(
                input(f'По указанному городу найдено {len(employers_list)} компаний, разместивших вакансии.\n'
                      f'Введите количество компаний по которым искать вакансии от 0 до {len(employers_list)}, '
                      f'если ввести "0" и нажать "Enter", то будут выбраны все найденные компании: '))
            # if num_employer > 20:
            # pause_get = 20  # Увеличиваем время паузы между запросами, чтобы сайт HH.ru не оборвал соединение
            if num_employer == 0:
                num_employer = len(employers_list)
        except ValueError:
            print(f'Ошибка ошибка ввода! Введите целое число от 0 до {len(employers_list)}')

    # Получаем список количества id работодателей, которое указал пользователь
    count = 0
    employers_list_id = []
    for employer in employer_id_name:
        if count < num_employer:
            employers_list_id.append(employer)
            count += 1
        elif num_employer == "":
            employers_list_id.append(employer)

    #  Получаем список словарей словарей вакансий каждого работодателя
    result_data = []
    for employer, name in employer_id_name.items():
        vacancies = hh_api.get_vacancies_by_employers(employer, city_id)
        result_data.append({'employer': employer, 'name': name, 'vacancies': vacancies})

    for item in result_data:

        print(item)
        print(type(item))

    # создаем экземпляр класса DBCreate
    db = DBCreate()
    # conn = DBCreate()  # Создаем экземпляр, класса открываем подключение
    db.create_database(database_name)
    db.create_tables(database_name)

    db.save_info_to_database(database_name, result_data)

    print(repr(db))
