import requests
from itertools import count
from math_tools import predict_rub_salary
from dotenv import load_dotenv
import os

def get_superjob_vacancies(language, page):
    load_dotenv()
    sj_api = os.environ["SJ_API"]
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": sj_api
    }
    elem_per_page = 100
    industry_id = 48
    params = {
        "catalogues": industry_id,
        "town": "Moscow",
        "keyword": {language},
        "page": page,
        "count": elem_per_page
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_superjob_statistics():
    languages = ["Python","Java","PHP","C++","C#","Ruby","go","1c"]
    profession_statistics_sj = {}

    for language in languages:
        summa = 0
        sum = 0
        vacancies_processed = 0
        average_salary = 0

        for page in count(0):
            vacancies = get_superjob_vacancies(language, page)

            for vacancy in vacancies['objects']:
                salary_from = vacancy['payment_from']
                salary_to = vacancy['payment_to']

                if vacancy["currency"] == 'rub':
                    salary = predict_rub_salary(salary_from,salary_to)
                    sum = sum + salary
                    vacancies_processed+=1

        if vacancies_processed:
            average_salary = round(sum/vacancies_processed)

        profession = {
            "vacancies_found": vacancies["total"],
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
        profession_statistics_sj[language] = profession
    return profession_statistics_sj
