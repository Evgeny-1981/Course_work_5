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
        return f'Ожидайте, выполняется подключение класса {self.__class__.__name__} к Postgres...\n'

    def create_tables(self, database_name: str):
        """Метод создает таблицы employers и vacancies в базе данных"""

        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id serial primary key,
                        company_id int,
                        employer_name varchar(255) not null,
                        employer_url varchar(255)
                        )
                        """)

                cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id serial primary key,
                        employer_id INT REFERENCES employers(employer_id),
                        vacancy_code int not null,
                        vacancy_city varchar(255) not null,
                        vacancy_name text not null,
                        salary_from int,
                        salary_to int,
                        currency varchar(3) not null, 
                        vacancy_url varchar(255) not null
                        )
                        """)
        cur.close()
        conn.close()

    def save_info_to_database(self, database_name: str, result_data: list[dict[str, any]]):
        """Метод сохраняет данные в таблицы базы данных"""
        conn = psycopg2.connect(dbname=database_name, **self.params_db)

        with conn.cursor() as cur:
            for employer in result_data:
                employer_id = employer['employer']
                employer_name = employer['name']
                employer_url = employer['employer_url']
                cur.execute(
                    """
                    INSERT INTO employers (company_id, employer_name, employer_url)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                    """,
                    (employer_id, employer_name, employer_url))
                employer_id = cur.fetchone()[0]
                vacancies_data = employer['vacancies']
                for vacancy in vacancies_data:
                    vacancy_code = vacancy['id']
                    vacancy_city = vacancy['area']['name']
                    vacancy_name = vacancy['name']
                    salary_from = vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] else 0
                    salary_to = vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] else 0
                    salary_currency = vacancy["salary"]["currency"] if vacancy["salary"] and vacancy["salary"][
                        "currency"] else 'НЕТ'
                    vacancy_url = vacancy['alternate_url']
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, vacancy_code, vacancy_city, vacancy_name, salary_from, 
                        salary_to, currency, vacancy_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, vacancy_code, vacancy_city, vacancy_name, salary_from, salary_to, salary_currency,
                         vacancy_url))

        conn.commit()
        conn.close()
