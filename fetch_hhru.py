import requests
from itertools import count
from math_tools import predict_rub_salary

def get_hh_vacancies(language, page):
    url = "https://api.hh.ru/vacancies"
    region = 1
    elem_per_page = 100
    params = {
        "text" : {language},
        "area" : region,
        "page": page,
        "per_page": elem_per_page
    } 
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()

def get_hh_statistic():
    languages = ["Python","Java","PHP","C++","C#","Ruby","go","1c"]
    profession_statistics_hhru = {}
    for language in languages:
        sum = 0
        vacancies_processed = 0

        for page in count(0):
            vacansies = get_hh_vacancies(language, page)
            if page >= vacansies["pages"] - 1:
                break
            for vacancy in vacansies["items"]:
                vacancy_salary = vacancy["salary"]
                
                
                if vacancy_salary and vacancy_salary["currency"] == 'RUR':
                    salary = vacancy["salary"]
                    salary_from = salary["from"]
                    salary_to = salary["to"]
                    calculated_salary  = predict_rub_salary(salary_from,salary_to)
                    sum = sum+calculated_salary
                    vacancies_processed+=1

            if vacancies_processed:
                average_salary = round(sum/vacancies_processed)
            else:
                print("vacancies_processed = 0")
                average_salary = 0

            profession = {
                "vacancies_found": vacansies["found"],
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
            }
            profession_statistics_hhru[language] = profession
 
    return profession_statistics_hhru