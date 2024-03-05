from statsmodels.stats.proportion import proportion_confint


def count_conf_int(n:int,N:int):
    """
    Расчет 95% ДИ для доли.
    n - частота встречаемости признака в группе
    N - общее количество наблюдений в выборке
    принтует результат в руссоком формате -
    вместо . в качестве разделителя десятичн дробей - ,
    """
    ci_low, ci_upp = proportion_confint(count = n,
                                        nobs = N,
                                        alpha=0.05,
                                        method='normal')
    ci_low = round(ci_low * 100, 2)
    ci_upp = round(ci_upp * 100, 2)
    percents = round((n * 100) / N, 2)
    result = f'{percents} [{ci_low}–{ci_upp}] %'
    # print(result.replace('.', ','))
    return {"percents": percents, "ci_low": ci_low, "ci_upp": ci_upp, "result_str": result}


if __name__ == '__main__':
    res = count_conf_int(n=50, N=100)
    print(res)