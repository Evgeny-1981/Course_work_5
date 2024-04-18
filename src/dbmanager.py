import psycopg2
from config import config


class DBManager:
    def __init__(self, database_name):
        self.params_db = config()
        self.database_name = database_name
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params_db)

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании. """
        with self.conn.cursor() as cur:
            cur.execute("""select e.employer_name, count(employer_id) from vacancies v
                        join employers e using(employer_id)
                        where e.employer_id = v.employer_id
                        group by e.employer_id order by count(employer_id) desc""")

            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""select e.employer_name, v.vacancy_name, concat(v.salary_from, '-', v.salary_to),
                        v.vacancy_url from vacancies v
                        join employers e using(employer_id)""")

            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""select avg((salary_from+salary_to)/2) from vacancies""")

            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""select v.vacancy_name, v.salary_from from vacancies v 
                        where salary_from > (select avg(salary_from+salary_to)/2 from vacancies)
                        order by salary_from desc""")

            return cur.fetchall()

    def get_vacancies_with_keyword(self, user_input):
        """Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python"""
        with self.conn.cursor() as cur:
            cur.execute(f"select * from vacancies where vacancy_name ilike '%{user_input}%'")

            return cur.fetchall()

    def quit(self) -> None:
        """ Закрывает соединение базой данных. """
        self.conn.close()
