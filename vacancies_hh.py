from datetime import date, timedelta

import requests

from api_halpers import predict_salary, show_table


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        salary = vacancy['salary']
        if salary['currency'] == 'RUR':
            salary_from = salary['from']
            salary_to = salary['to']
            predicted_salary = predict_salary(salary_from, salary_to)
            return predicted_salary


def get_vacancies_hh_information(language='Python',
                                 page=0, area=1,
                                 date_from=30):
    url = 'https://api.hh.ru/vacancies/'
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

    date_from = date.today() - timedelta(days=30)
    popular_languages_statistics = {}

    for language in popular_programming_languages:

        vacancies_hh_information = get_vacancies_hh_information(language=language,
                                                                date_from=date_from)
        pages_number = vacancies_hh_information['pages']
        page, total_salary, vacancies_processed = 0, 0, 0
        vacancy_counts = vacancies_hh_information['found']

        while page < pages_number:
            vacancies = get_vacancies_hh_information(language=language,
                                                     page=page,
                                                     date_from=date_from)['items']

            for vacancy in vacancies:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
            page += 1

        popular_languages_statistics[language] = {
            'vacancies_found': vacancy_counts,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }

    show_table(popular_languages_statistics, title='HeadHunter Москва')


if __name__ == '__main__':
    main()
