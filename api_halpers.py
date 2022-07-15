def predict_salary(salary_from, salary_to):
    predict_salary = None
    if salary_from and salary_to:
        predict_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predict_salary = salary_from * 1.2
    elif salary_to:
        predict_salary = salary_to * 0.8
    return predict_salary