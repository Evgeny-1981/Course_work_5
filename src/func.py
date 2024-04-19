from src.api import HeadHunterAPI
from src.dbcreate import DBCreate
from src.dbmanager import DBManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    database_name = 'coursework5'

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
        employer_id_name[employer_id] = employer_name['employer_name'], employer_name['employer_url']

    #  Получаем список id работодателей из словаря employers_dict
    employers_list = []
    for employer in employers_dict:
        employers_list.append(employer)

    #  Запрос количества id работодателей, по которым будет выполнен поиск вакансий
    num_employer = None
    while num_employer not in range(1, len(employer_id_name) + 1):
        try:
            num_employer = int(
                input(f'По указанному городу найдено {len(employer_id_name)} компаний, разместивших вакансии.\n'
                      f'Введите количество компаний по которым искать вакансии от 0 до {len(employer_id_name)}, '
                      f'если ввести "0" и нажать "Enter", то будут выбраны все найденные компании: '))
            if num_employer == 0:
                num_employer = len(employer_id_name)
        except ValueError:
            print(f'Ошибка ввода! Введите целое число от 0 до {len(employer_id_name)}')

    #  Получаем список словарей словарей вакансий каждого работодателя
    result_data = []
    count = 0
    for employer, name in employer_id_name.items():
        if count < num_employer:
            vacancies = hh_api.get_vacancies_by_employers(employer, city_id)
            result_data.append({'employer': employer, 'name': name[0], 'employer_url': name[1], 'vacancies': vacancies})
            count += 1

    #  Создаем экземпляр класса DBCreate
    db = DBCreate()
    print(repr(db))
    #  Создание базы данных
    db.create_database(database_name)
    #  Создание таблиц
    db.create_tables(database_name)
    #  Сохранение даных в таблицы
    db.save_info_to_database(database_name, result_data, city_name)
    #  Создаем экземпляр класса DBManager для подключения к БД
    conn = DBManager(database_name)
    print("Данные получены и записаны в базу данных. Выберите дальнейшие действия:")
    while True:
        try:
            user_input = int(input("""
        1 - Вывести список всех компаний и количество их вакансий.
        2 - Вывести список всех вакансий с указанием названия компании, вакансии, зарплаты, ссылки на вакансию.
        3 - Вывести среднюю зарплату по вакансиям.
        4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        5 - Вывести список всех вакансий, в названии которых содержатся переданные в метод слова.
        0 - Для завершения программы.\n"""))

            if user_input == 1:
                print('\n' * 100)
                query_1 = DBManager.get_companies_and_vacancies_count(conn)
                for i, row in enumerate(query_1, 1):
                    print(f"{i}.Компания: '{row[0]}', количество вакансий: {row[1]}")
                continue
            elif user_input == 2:
                print('\n' * 100)
                query_2 = DBManager.get_all_vacancies(conn)
                for i, row in enumerate(query_2, 1):
                    print(f"{i}.Компания: '{row[0]}', вакансия: '{row[1]}', зарплата: '{row[2]}', URL: '{row[3]}'")
                continue
            elif user_input == 3:
                print('\n' * 100)
                query_3 = DBManager.get_avg_salary(conn)
                for row in query_3:
                    print(f"Средняя зарплата по всем имеющимся вакансиям в базе данных: {round(float(row[0]), 2)} у.е.")
                continue
            elif user_input == 4:
                print('\n' * 100)
                query_4 = DBManager.get_vacancies_with_higher_salary(conn)
                print(f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
                for i, row in enumerate(query_4, 1):
                    print(f"{i}. {row[0]}, зарплата {row[1]}")
                continue
            elif user_input == 5:
                print('\n' * 100)
                query_5 = DBManager.get_vacancies_with_keyword(conn, user_input=input(
                    "Введите искомое слово в названии вакансии: "))
                print(f"Найдено {len(query_5)} вакансий:")
                for i, row in enumerate(query_5, 1):
                    print(f"{i}. Вакансия: {row[3]}, ссылка на вакансию: {row[6]}")
                continue
            elif user_input == 0:
                print('Выполнение программы завершено.')
                DBManager.quit(conn)
                break

        except ValueError:
            print(f'Ошибка ввода! Введите целое число от 0 до 5')
