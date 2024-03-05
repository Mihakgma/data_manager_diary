# chi-squared test with similar proportions
from scipy.stats import chi2_contingency
from scipy.stats import chi2
# Критерий Фишера
from scipy.stats import fisher_exact
from numpy import nan as np_nan


def chi_squaredtest(table):

    stat, p, dof, expected = chi2_contingency(table)

    print('dof=%d' % dof)
    # print(expected)
    # interpret test-statistic
    prob = 0.95
    critical = chi2.ppf(prob, dof)
    print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')
    # interpret p-value
    alpha = 1.0 - prob
    print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')

    return stat, p, dof, expected


def chisq_fisher_tests(lst1: list, lst2:list):
    pity_frequency = False
    curr_stats = '-'
    curr_p_value = '-'
    black_list = ['', 0, np_nan]

    print(lst1)
    print(lst2)

    if any([i in lst1 for i in black_list]) or any([i in lst2 for i in black_list]):
        return curr_stats, curr_p_value
    if len(lst1) != 2 or len(lst2) != 2:
        raise ValueError("На вход функции должны быть поданы листы, содержащие 2 элемента (длина листа == 2)!")

    for current_lst in [lst1, lst2]:
        for elem in current_lst:
            if elem < 5:
                pity_frequency = True
    # формируем таблицу сопряженности (список листов)
    curr_cont_table = [lst1, lst2]

    if pity_frequency:
        try:
            fisher = fisher_exact(curr_cont_table, alternative='two-sided')
        except ValueError:
            return curr_stats, curr_p_value
        #fisher_exact возвращает 2 переменные - oddsr, p
        curr_stats = '-'
        curr_p_value = round(fisher[1], 3)

    elif not(pity_frequency):
        xi_square_results = chi_squaredtest(curr_cont_table)
        #print('Хи-Квадрат посчитан')
        curr_stats = round(xi_square_results[0], 2)
        curr_p_value = round(xi_square_results[1], 5)

    return curr_stats, curr_p_value


if __name__ == '__main__':
    lst_1 = [5, 10]
    lst_2 = [30, 99]
    res = chisq_fisher_tests(lst1=lst_1,
                             lst2=lst_2)
    print(res)
