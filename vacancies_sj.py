from dotenv import load_dotenv
import requests
import os
from api_halpers import predict_salary


def get_vacancies_sj_information(secret_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'catalogues': 48,
        'town': 'Москва'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['objects']


def predict_rub_salary_for_superJob():
    pass


def predict_rub_salary_sj(vacancy):
    pass


def main():

    load_dotenv()
    super_job_secret_key = os.getenv("SUPER_JOB_SECRET_KEY")
    
    vacancies_sj_information = get_vacancies_sj_information(super_job_secret_key)
    
    for vacancy in vacancies_sj_information:
        print(f"{vacancy['profession']}, {vacancy['town']['title']}")
        
        
if __name__ == '__main__':
    main()