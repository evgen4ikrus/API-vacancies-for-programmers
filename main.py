import requests
from datetime import date, timedelta


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
        params = {
            'text': f'Программист {language}',
            'area': '1',
            'date_from': date_from,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        vacancies = response.json()['items']
        total_salary = 0
        vacancies_processed = 0
        vacancy_counts = response.json()['found']
        
        for vacancy in vacancies:
            salary = predict_rub_salary(vacancy)
            if salary:
                vacancies_processed += 1
                total_salary += salary
        
        popular_vacancies_statistics[language] = {
            'vacancies_found': vacancy_counts,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }
            
    params = {
        'text': f'Программист Python',
        'area': '1',
        'date_from': date_from,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    print(popular_vacancies_statistics)
    

if __name__ == '__main__':
    main()