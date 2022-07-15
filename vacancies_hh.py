import requests
from datetime import date, timedelta
from api_halpers import predict_salary


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        salary = vacancy['salary']
        if salary['currency'] == 'RUR':
            salary_from = salary['from']
            salary_to = salary['to']
            predicted_salary = predict_salary(salary_from, salary_to)
            return predicted_salary


def get_vacancies_hh_information(url, language, page=0, area=1, date_from=30):
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
        vacancies_hh_information = get_vacancies_hh_information(url, language, date_from=date_from)
        page = 0
        pages_number = vacancies_hh_information['pages']
        total_salary = 0
        vacancies_processed = 0
        
        while page < pages_number:  
            vacancies_hh_information = get_vacancies_hh_information(url, language, page, date_from=date_from)
            vacancies = vacancies_hh_information['items']
            vacancy_counts = vacancies_hh_information['found']

            for vacancy in vacancies:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
            page += 1
            
        popular_vacancies_statistics[language] = {
            'vacancies_found': vacancy_counts,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }   
    
    print(popular_vacancies_statistics)
        
if __name__ == '__main__':
    main()