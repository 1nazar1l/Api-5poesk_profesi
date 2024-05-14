def predict_rub_salary(salary_from,salary_to):
    if salary_from == 0 or salary_from is None:
        return salary_to*0.8
    elif salary_to == 0 or salary_to is None:
        return salary_from * 1.2
    else:
        return (salary_from + salary_to)/2