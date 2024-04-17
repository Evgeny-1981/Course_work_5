import psycopg2
from config import config


class DBManager:
    def __init__(self, database_name, params):
        self.params_db = params
        self.database_name = database_name
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params_db)

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании. """
        with self.conn.cursor()as cur:
            cur.execute("""SELECT E.employer_name, count(employer_id) from vacancies V
                        join employers E using(employer_id)
                        where E.employer_id = V.employer_id
                        group by E.employer_id """)

            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""select e.employer_name, v.vacancy_name, CONCAT(v.salary_from, '-', v.salary_to),
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
            cur.execute("""select * from vacancies 
                        where salary_from > (select avg((salary_from+salary_to)/2) from vacancies)""")
            answer = cur.fetchall()
        return answer

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python"""
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM  vacancies WHERE vacancy_name LIKE '%{word}%'")
            answer = cur.fetchall()
        return answer
