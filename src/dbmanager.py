import psycopg2


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
            answer = cur.fetchall()
        return answer

    def get_all_vacancies():
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM  vacancies')
            answer = cur.fetchall()
        return answer

    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute('SELECT AVG(salary) FROM  vacancies')
            answer = cur.fetchall()
        return answer

    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM  vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
            answer = cur.fetchall()
        return answer

    def get_vacancies_with_keyword():
        """Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python"""
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM  vacancies WHERE vacancy_name LIKE '%{word}%'")
            answer = cur.fetchall()
        return answer
