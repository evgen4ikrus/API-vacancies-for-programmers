from dotenv import load_dotenv
import requests
from datetime import date, timedelta
import os

def predict_rub_salary(vacancy):
    if vacancy['salary']:
        salary = vacancy['salary']
        if salary['currency'] == 'RUR':
            if salary['from'] and salary['to']:
                return (salary['from'] + salary['to']) / 2
            elif salary['from']:
                return salary['from'] * 1.2
            elif salary['to']:
                return salary['to'] * 0.8


def get_vacancies_information(url, language, page=0, area=1, date_from=30):
    params = {
            'text': f'Программист {language}',
            'area': area,
            'date_from': date_from,
            'page': page,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def main():

    load_dotenv()
    super_job_secret_key = os.getenv("SUPER_JOB_SECRET_KEY")

    popular_programming_languages = [
        'Python',
        'Java',
        'Javascript',
        'Go',
        'C',
        'C#',
        'C++',
        'PHP',
        'Ruby',
    ]


    url = 'https://api.hh.ru/vacancies/'
    date_from = date.today() - timedelta(days=30)
    popular_vacancies_statistics = {}

    for language in popular_programming_languages:
        vacancies_information = get_vacancies_information(url, language, date_from=date_from)
        page = 0
        pages_number = vacancies_information['pages']
        pages_number = 1
        total_salary = 0
        vacancies_processed = 0
        
        while page < pages_number:  
            vacancies_information = get_vacancies_information(url, language, page, date_from=date_from)
            vacancies = vacancies_information['items']
            vacancy_counts = vacancies_information['found']

            for vacancy in vacancies:
                salary = predict_rub_salary(vacancy)
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
            page += 1
            
        popular_vacancies_statistics[language] = {
            'vacancies_found': vacancy_counts,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }   

    
if __name__ == '__main__':
    main()