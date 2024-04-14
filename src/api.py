import time

import requests
from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Создаем абстрактный класс для HeadHunterAPI"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_city_id(self, query):
        pass

    @abstractmethod
    def get_employers(self, city_id):
        pass

    @abstractmethod
    def get_vacancies_by_employers(self, employer, city_id):#, pause_get):
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для получения кода города, списка работодателей и их вакансий с сайта HeadHanter"""
    id_employer: list  # Список работадателей
    id_area: str  # Код города
    employer_vacancies: list  # Список вакансий

    def __init__(self, id_employer=None, id_area=None):
        self.pause_get = None
        self.employer = None
        self.city_name = None
        self.city_id = None
        self.url_areas = "https://api.hh.ru/areas"
        self.url_vacancies = f"https://api.hh.ru/vacancies"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'}


    def __repr__(self):
        return f'Ожидайте, выполняется подключение класса {self.__class__.__name__} к сайту HH...\n'

    def get_city_id(self, query_city):
        """Метод получает id города, который ввел пользователь, для поиска работодателей"""
        response = requests.get(self.url_areas)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

        for country in data:
            for region in country['areas']:
                if region['name'] == query_city:
                    area_id = region['id']
                    return area_id
                for city in region['areas']:
                    if city['name'] == query_city:
                        area_id = city['id']
                        return area_id

    def get_employers(self, city_id):
        """Метод получает компании по указанному городу в виде id и возвращает отсортированный словарь работодателей
        по начальной зарплате"""
        vacancies = []
        params = {'page': 0, 'per_page': 100, 'area': city_id}
        while params.get('page') != 20:
            response = requests.get(self.url_vacancies, params=params, headers=self.headers)
            if response.status_code == 200:
                vacancy = response.json()['items']

                vacancies.extend(vacancy)
                params['page'] += 1
            else:
                print(f"Error: {response.status_code}")
                return None

        employers_dict = {}
        for vacancy in vacancies:
            if vacancy['employer'].get('id') is not None:
                employer_id = vacancy['employer']['id']
                employer_name = vacancy['employer']['name']
                salary_from = vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] else 0
                employers_dict[employer_id] = {'employer_name': employer_name, 'salary_from': salary_from}

        sorted_employers_dict = dict(
            sorted(employers_dict.items(), key=lambda item: item[1]['salary_from'], reverse=True))

        return sorted_employers_dict

    def get_vacancies_by_employers(self, employer, city_id):#, pause_get:float):
        """Метод получает список словарей вакансий по переданным работодателям"""
        params = {'page': 0, 'per_page': 100, 'employer_id': {employer}, 'area': {city_id}}
        employer_vacancies = []
        while params.get('page') != 100:
            response = requests.get(self.url_vacancies, params=params, headers=self.headers)
            params['page'] += 1
            if response.status_code == 200:
                vacancy = response.json()['items']
                employer_vacancies.extend(vacancy)
                # time.sleep = pause_get
                return employer_vacancies
            else:
                print(f"Error: {response.status_code}")
                return None
