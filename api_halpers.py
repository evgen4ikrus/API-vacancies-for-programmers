from terminaltables import AsciiTable


def get_table(languages_statistics,
               title='Название таблицы'):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ],
    ]
    for language_statistics in languages_statistics:
        table_data.append(
            [
                language_statistics,
                languages_statistics[language_statistics]['vacancies_found'],
                languages_statistics[language_statistics]['vacancies_processed'],
                languages_statistics[language_statistics]['average_salary'],
            ]
        )
    table = AsciiTable(table_data, title).table
    return table


def predict_salary(salary_from, salary_to):
    predict_salary = None
    if salary_from and salary_to:
        predict_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predict_salary = salary_from * 1.2
    elif salary_to:
        predict_salary = salary_to * 0.8
    return predict_salary
