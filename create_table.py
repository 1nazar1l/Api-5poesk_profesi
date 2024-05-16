from fetch_hhru import get_hh_statistic
from fetch_superjob import get_superjob_statistics
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os

def create_table(lang_statistic,title):
    vacancies_table = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]]
    for language,statistic in lang_statistic.items():
        vacancies_table.append([
            language,
            statistic["vacancies_found"],
            statistic["vacancies_processed"],
            statistic["average_salary"],
        ])
    table = AsciiTable(vacancies_table, title)
    return table

def main():
    load_dotenv()
    sj_api_token = os.environ["SJ_API_TOKEN"]
    title_sj = "SuperJob Moscow"
    title_hh = "HeadHunter Moscow"
    sj_statistic = get_superjob_statistics()
    hh_statistic = get_hh_statistic()
    sj_table = create_table(sj_statistic, title_sj, sj_api_token)
    hh_table = create_table(hh_statistic, title_hh)
    print(sj_table.table)
    print(hh_table.table)

if __name__ == "__main__":
    main()