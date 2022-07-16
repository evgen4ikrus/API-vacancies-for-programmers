from dotenv import load_dotenv
import requests
import os
from api_halpers import predict_salary, show_table
import math


def get_vacancies_sj_information(secret_key, id_category=48, language='Python', page=0, town='Москва'):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'catalogues': id_category,
        'town': town,
        'keyword': language,
        'page': page,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_sj(vacancy):
    payment_from = vacancy['payment_from']
    payment_to = vacancy['payment_to']
    predicted_salary = predict_salary(payment_from, payment_to)
    return predicted_salary


def main():
    
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

    load_dotenv()
    super_job_secret_key = os.getenv("SUPER_JOB_SECRET_KEY")
    popular_languages_statistics = {}
    city = 'Москва'

    for language in popular_programming_languages:

        vacancies_sj_information = get_vacancies_sj_information(super_job_secret_key, language=language, town=city)
        vacancies_found = vacancies_sj_information['total']
        pages_number = math.ceil(vacancies_found / 20)
        page, total_salary, vacancies_processed = 0, 0, 0

        while page < pages_number:  
            vacancies = get_vacancies_sj_information(super_job_secret_key, language=language, page=page, town=city)['objects']

            for vacancy in vacancies:
                salary = predict_rub_salary_sj(vacancy)
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
            page += 1

        popular_languages_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }  

    show_table(popular_languages_statistics, title=f'SuperJob {city}')
    

if __name__ == '__main__':
    main()
    
    
    
    