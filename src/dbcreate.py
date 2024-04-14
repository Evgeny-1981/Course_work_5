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
        """Метод сохраняет анные в таблицы базы данных"""
        conn = psycopg2.connect(dbname=database_name, **self.params_db)

        with conn.cursor() as cur:
            for employer in result_data:
                employer_data = employer['employer']

                employer_name = employer['vacancies']['employer']['name']
                cur.execute(
                    """
                    INSERT INTO channels (title, views, subscribers, videos, channel_url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING channel_id
                    """,
                    (channel_data['title'], channel_stats['viewCount'], channel_stats['subscriberCount'],
                     channel_stats['videoCount'], f"https://www.youtube.com/channel/{channel['channel']['id']}")
                )
                channel_id = cur.fetchone()[0]
                videos_data = channel['videos']
                for video in videos_data:
                    video_data = video['snippet']
                    cur.execute(
                        """
                        INSERT INTO videos (channel_id, title, publish_date, video_url)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (channel_id, video_data['title'], video_data['publishedAt'],
                         f"https://www.youtube.com/watch?v={video['id']['videoId']}")
                    )

        conn.commit()
        conn.close()

        with (psycopg2.connect(dbname=database_name, **self.params_db) as conn):
            with conn.cursor() as cur:
                for key, value in employers_dict.items():
                    cur.execute(f"INSERT INTO employers(company_id, employer_name, employer_url) "
                                f"values({key}, $${value["employer_name"]}$$"
                                f", '{value["employer_url"]}')")
                for vacancy in vacancies_list:
                    salary_from = vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] else 0
                    salary_to = vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] else 0
                    salary_currency = vacancy["salary"]["currency"] if vacancy["salary"] and vacancy["salary"]["currency"] else 'НЕТ'
                    cur.execute(f"INSERT INTO vacancies(employer_id, vacancy_code, vacancy_city, vacancy_name, salary_from, "
                                f"salary_to, currency, vacancy_url) values('{vacancy['employer']['id']}', '{vacancy['id']}',"
                                f"'{vacancy['area']['name']}', "
                                f"$${vacancy['name']}$$, "
                                f"'{salary_from}', "
                                f"'{salary_to}', "
                                f"'{salary_currency}', "
                                f"'{vacancy['alternate_url']}')")

        conn.close()
