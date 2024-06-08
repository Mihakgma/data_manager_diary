from pandas import Series as pd_Series
# SE (Standard Error) function, IQR, skew, kurtosis, kstest, shapiro, mannwhitneyu
from scipy.stats import sem, iqr, skew, kurtosis, kstest, shapiro, mannwhitneyu


def count_quantitative_vars(values: pd_Series,
                            result_df_colnames: list,
                            depending_variable: str,
                            group_variable_value,
                            not_used_colnames_number: int = 3,
                            round_digits: int = 3):
    values = values.apply(lambda x: int(x) if type(x) != float else x)
    # curr_col_descr_stats = values.describe()
    curr_col_descr_stats = values.dropna().describe()
    curr_col_descr_stats_lst = curr_col_descr_stats.to_list()

    N = curr_col_descr_stats_lst[0]
    M = round(curr_col_descr_stats_lst[1], round_digits)
    SD = round(curr_col_descr_stats_lst[2], round_digits)
    variability_coeff = round(SD / M, round_digits)
    Min = round(curr_col_descr_stats_lst[3], round_digits)
    Max = round(curr_col_descr_stats_lst[7], round_digits)
    lower_quart = round(curr_col_descr_stats_lst[4], round_digits)
    Me = round(curr_col_descr_stats_lst[5], round_digits)
    higher_quart = round(curr_col_descr_stats_lst[6], round_digits)
    IQR = round(iqr(values.to_list()), round_digits)
    SE = round(sem(values.to_list()), round_digits)
    kstest_res = kstest(values.to_list(), 'norm')
    # kstest_res[1]
    KS_p_value = round(kstest_res[1], round_digits)
    shapiro_test = shapiro(values.to_list())
    SW_p_value = round(shapiro_test.pvalue, round_digits)
    skew_value = round(skew(values.to_list()), round_digits)
    kurtosis_value = round(kurtosis(values.to_list()), round_digits)
    Mo = max(set(values.to_list()), key=values.to_list().count)

    # наполняем список значениями
    values_lst = [
        depending_variable,
        group_variable_value,
        M, SE, SD, Min, Max, variability_coeff,
        Me, lower_quart, higher_quart, IQR,
        KS_p_value, SW_p_value, skew_value, kurtosis_value
    ]
    result_lst = []
    for val in values_lst:
        result_lst.append(val)
    columns_num_must_be = len(result_df_colnames) - not_used_colnames_number
    if len(result_lst) != columns_num_must_be:
        raise ValueError(f"количество показателей не совпадает: {len(result_lst)} (расч)vs{columns_num_must_be}(должн)")

    return result_lst


def compute_mannwhitney(data1, data2, round_digits: int = 3):
    stat_out, p_out = mannwhitneyu(data1.dropna(),
                                   data2.dropna(),
                                   alternative='two-sided')
    return round(stat_out, round_digits), round(p_out, round_digits)

