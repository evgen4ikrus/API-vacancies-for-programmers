import requests
from datetime import date, timedelta

    
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
    vacancy_counts = {}

    for language in popular_programming_languages:
        params = {
        'text': f'Программист {language}',
        'area': '1',
        'date_from': date_from,
    }
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancy_counts[language] = response.json()['found']

    params = {
        'text': f'Программист Python',
        'area': '1',
        'date_from': date_from,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    vacancies = response.json()['items']
    for vacancy in vacancies:
        print(vacancy['salary'])

if __name__ == '__main__':
    main()