import psycopg2
from config import config


class DBCreate:
    """Класс для создания базы данных и таблиц"""

    def __init__(self):

        self.params_db = config()

    def create_database(self, database_name: str):
        """Создание базы данных."""

        conn = psycopg2.connect(dbname='postgres', **self.params_db)
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

    def __repr__(self):
        return (f'Ожидайте, выполняется подключение класса {self.__class__.__name__} к СУБД PostgeSQL.\n'
                f'Создаем базу данных, таблицы и заполняем их...')

    def create_tables(self, database_name: str):
        """Метод создает таблицы employers и vacancies в базе данных"""

        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id serial primary key,
                        employer_name varchar(255) not null,
                        employer_url varchar(255)
                        )
                        """)

                cur.execute("""
                    CREATE TABLE city (
                        city_id serial primary key,
                        city varchar(255) not null
                        )
                        """)

                cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id serial primary key,
                        employer_id INT REFERENCES employers(employer_id),
                        city_id int REFERENCES city(city_id),
                        vacancy_name text not null,
                        salary_from int,
                        salary_to int,
                        vacancy_url varchar(255) not null
                        )
                        """)
        cur.close()
        conn.close()

    def save_info_to_database(self, database_name: str, result_data: list[dict[str, any]], city_name: str):
        """Метод сохраняет данные в таблицы базы данных"""
        conn = psycopg2.connect(dbname=database_name, **self.params_db)

        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO city (city) values ('{city_name}') RETURNING city_id")
            city_id = cur.fetchone()[0]
            for employer in result_data:
                employer_name = employer['name']
                employer_url = employer['employer_url']
                cur.execute(
                    """
                    INSERT INTO employers (employer_name, employer_url)
                    VALUES (%s, %s)
                    RETURNING employer_id
                    """,
                    (employer_name, employer_url))
                employer_id = cur.fetchone()[0]
                vacancies_data = employer['vacancies']
                for vacancy in vacancies_data:
                    vacancy_name = vacancy['name']
                    salary_from = vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] else 0
                    salary_to = vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] else 0
                    vacancy_url = vacancy['alternate_url']
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, city_id, vacancy_name, salary_from, salary_to, vacancy_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, city_id, vacancy_name, salary_from, salary_to, vacancy_url))

        conn.commit()
        conn.close()
