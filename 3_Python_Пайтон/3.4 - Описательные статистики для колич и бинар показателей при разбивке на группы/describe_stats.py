from pandas import DataFrame as pd_DataFrame

from numpy import mean as np_mean
from numpy import median as np_median
from numpy import nan as np_nan

# handmade modules
from proportion_conf_intervals import count_conf_int
from chi_sqared_fisher_tests import chisq_fisher_tests
from quant_vars_computations import count_quantitative_vars, compute_mannwhitney
from bootstrap import get_bootstrap


class Describer:
    """
    this class helps to calculate descriptive statistics (for nominal and quantitative variables) in
    pandas dataframe after grouping
    """
    __nomin_colnames = {
        "RU": ["показатель", "группа", "N", 'n', "доля_%", "ДИ-", "ДИ+", "статистика_знач", "p_уровень_значимости"],
        "EN": ["variable", "group", "N", 'n', "percentage_%", "CI-", "CI+", "statistic_value", "p_value"]
    }
    __quant_colnames = {
        "RU": ["показатель", "группа", "среднее", "ст_ош", "ст_откл", "мин", "макс", "коэф_вариабельности",
               "медиана", "25%", "75%", "МКР",
               "КС_p_уровень", "ШУ_p_уровень", "наклон", "эксцесс", "МУ_статистика", "МУ_p_уровень", "бутст_p_уровень"],
        "EN": ["variable", "group", "mean", "SE", "SD", "min", "max", "variability_coeff",
               "median", "25%", "75%", "IQR",
               "KS_p_value", "SW_p_value", "skew", "kurtosis", "MW_statistic", "MW_p_value", "bootstrap_p_value"]
    }

    def __init__(self, df: pd_DataFrame):
        self.df = df
        self.__computations = []

    def get_df(self):
        return self.__df

    def set_df(self, df):
        if type(df) != pd_DataFrame:
            raise TypeError("атрибут df должен представлять из себя пандас-ДФ!")
        self.__df = df

    df = property(get_df, set_df)

    def __check_colnames(self, grouping_var_name, analyzed_var_names):
        df = self.df
        df_colnames = list(df)
        if type(grouping_var_name) != str or grouping_var_name not in df_colnames:
            raise ValueError(f"проверьте название группирующей переменной: <{grouping_var_name}>")
        if any([colname not in df_colnames for colname in analyzed_var_names]):
            raise ValueError(f"проверьте названия анализируемых столбцов ДФ: <{analyzed_var_names}>")

    def compute_quantitative_variables(self,
                                       grouping_variable_name: str,
                                       quantitative_variable_names: list,
                                       colnames_lang: str="RU",
                                       boot_iterations: int=10000,
                                       boot_statistic=np_median,
                                       get_total_row: bool = True,
                                       compute_mean: bool = True,
                                       compute_min: bool = True,
                                       compute_max: bool = True,
                                       compute_se: bool = True,
                                       compute_sd: bool = True,
                                       compute_median: bool = True,
                                       compute_percentiles: bool = True,
                                       compute_iqr: bool = True,
                                       compute_variability_coefficient: bool = True,
                                       compute_skew: bool = True,
                                       compute_kurtosis: bool = True,
                                       compute_kolmogorov_smirnov: bool = True,
                                       compute_shapiro_wilks: bool = True,
                                       compute_mannwhitney_test: bool = True,
                                       compute_wilcoxson_test: bool = True,
                                       compute_bootstrap: bool = True,
                                       bootstrap_iter_number: int = 1000,
                                       bootstrap_statistic=np_mean,
                                       bootstrap_conf_level=0.95):
        """

        :param grouping_variable_name:
        :param quantitative_variable_names:
        :param get_total_row: compute descriptive stats for all sample without grouping variable (influence)
        :param compute_mean:
        :param compute_se: standard error of the mean value
        :param compute_sd: standard deviation
        :param compute_median: 50%-th percentile
        :param compute_percentiles: 25% and 75% percentiles
        :param compute_iqr: interquartile range
        :param compute_variability_coefficient:
        :param compute_skew:
        :param compute_kurtosis:
        :param compute_kolmogorov_smirnov:
        :param compute_shapiro_wilks:
        :param compute_mannwhitney_test:
        :param compute_wilcoxson_test:
        :param compute_bootstrap: get only p-value of the bootstrap computation result
        :param bootstrap_iter_number: 100-10000 recommend info
        :param bootstrap_statistic: mean, median etc
        :param bootstrap_conf_level:
        :return:
        """

        self.__check_colnames(grouping_var_name=grouping_variable_name,
                              analyzed_var_names=quantitative_variable_names)
        df = self.df
        grouping_var_vals = list(df[grouping_variable_name].unique())
        grouping_var_vals.sort()
        if len(grouping_var_vals) != 2:
            print("Бинарная переменная должна иметь 2 вариации признака!")
            raise ValueError(f"Вариативность группирующей переменной составил: {len(grouping_var_vals)}!")
        out_df_colnames = self.__quant_colnames[colnames_lang]
        # пустой ДФ для дальнейшего наполнения
        df_out = pd_DataFrame(columns=out_df_colnames)
        empty = '-'
        for column_name in quantitative_variable_names:
            column_name = column_name.strip()
            print(f"\n<{column_name}>")
            values_sample_t = []
            values_sample_1 = []
            values_sample_2 = []
            gr_var_val_1 = grouping_var_vals[0]
            gr_var_val_2 = grouping_var_vals[1]
            sample_1 = df[column_name][df[grouping_variable_name] == gr_var_val_1].apply(lambda x:
                                                                                         np_nan
                                                                                         if str(x).strip() in ("","-")
                                                                                         else x)
            values_sample_1 = count_quantitative_vars(values=sample_1,
                                                      result_df_colnames=out_df_colnames,
                                                      depending_variable=column_name,
                                                      group_variable_value=gr_var_val_1)

            sample_2 = df[column_name][df[grouping_variable_name] == gr_var_val_2].apply(lambda x:
                                                                                         np_nan
                                                                                         if str(x).strip() in ("","-")
                                                                                         else x)
            values_sample_2 = count_quantitative_vars(values=sample_2,
                                                      result_df_colnames=out_df_colnames,
                                                      depending_variable=column_name,
                                                      group_variable_value=gr_var_val_2)
            mw_res = compute_mannwhitney(data1=sample_1, data2=sample_2)

            boot_result = get_bootstrap(data_column_1=sample_1,  # числовые значения первой выборки
                                        data_column_2=sample_2,  # числовые значения второй выборки
                                        boot_it=boot_iterations,  # количество бутстрэп-подвыборок
                                        statistic=boot_statistic)
            for i in mw_res:
                values_sample_1.append(i)
            values_sample_1.append(boot_result["p_value"])
            for i in range(3):
                values_sample_2.append(empty)

            # Общее для всех (сумма обоих выборок)
            sample_t = df[column_name].apply(lambda x: np_nan if str(x).strip() in ("","-") else x)
            values_sample_t = count_quantitative_vars(values=sample_t,
                                                      result_df_colnames=out_df_colnames,
                                                      depending_variable=column_name,
                                                      group_variable_value=empty)
            for i in range(3):
                values_sample_t.append(empty)
            # наполяем ДФ расчитанными значениями
            rows_num = df_out.shape[0]
            for row in [values_sample_t,
                        values_sample_1,
                        values_sample_2]:
                df_out.loc[rows_num] = row
                rows_num +=1
        return df_out


    def calculate_descr_stats_binar_vars(self,
                                         grouping_variable_name,
                                         analyzed_variable_names,
                                         colnames_lang: str="RU"):
        self.__check_colnames(grouping_var_name=grouping_variable_name,
                              analyzed_var_names=analyzed_variable_names)
        df = self.df
        grouping_var_vals = list(df[grouping_variable_name].unique())
        grouping_var_vals.sort()
        if len(grouping_var_vals) != 2:
            print("Бинарная переменная должна иметь 2 вариации признака!")
            raise ValueError(f"Вариативность группирующей переменной составил: {len(grouping_var_vals)}!")
        # print(type(grouping_var_vals))
        out_df_colnames = self.__nomin_colnames[colnames_lang]
        # print(grouping_var_vals)
        # пустой ДФ для дальнейшего наполнения
        df_out = pd_DataFrame(columns=out_df_colnames)
        # df_out.columns = out_df_colnames
        for column_name in analyzed_variable_names:
            column_name = column_name.strip()
            print(f"\n<{column_name}>")
            values_sample_t = []
            values_sample_1 = []
            values_sample_2 = []
            gr_var_val_1 = grouping_var_vals[0]
            gr_var_val_2 = grouping_var_vals[1]
            sample_1 = df[column_name][df[grouping_variable_name] == gr_var_val_1].apply(lambda x:
                                                                                         np_nan
                                                                                         if str(x).strip() in ("","-")
                                                                                         else x)
            sample_2 = df[column_name][df[grouping_variable_name] == gr_var_val_2].apply(lambda x:
                                                                                         np_nan
                                                                                         if str(x).strip() in ("","-")
                                                                                         else x)

            N_1 = len(sample_1)
            N_2 = len(sample_2)
            n_1 = sum(sample_1.dropna())
            n_2 = sum(sample_2.dropna())
            prop_res_1 = count_conf_int(n=n_1, N=N_1)
            prop_res_2 = count_conf_int(n=n_2, N=N_2)
            percents_1, ci_low_1, ci_upp_1 = prop_res_1["percents"], prop_res_1["ci_low"], prop_res_1["ci_upp"]
            percents_2, ci_low_2, ci_upp_2 = prop_res_2["percents"], prop_res_2["ci_low"], prop_res_2["ci_upp"]
            stats, p_value = chisq_fisher_tests(lst1=[n_1, N_1], lst2=[n_2, N_2])

            # Общее для всех (сумма обоих выборок)
            empty = '-'
            sample_t = df[column_name].apply(lambda x: np_nan if str(x).strip() in ("","-") else x)
            N_t = len(sample_t)
            n_t = sum(sample_t.dropna())
            prop_res_t = count_conf_int(n=n_t, N=N_t)
            percents_t, ci_low_t, ci_upp_t = prop_res_t["percents"], prop_res_t["ci_low"], prop_res_t["ci_upp"]
            # наполяем списки расчитанными значениями
            for (v_t, v_1, v_2) in zip([column_name, empty, N_t, n_t, percents_t, ci_low_t, ci_upp_t, empty, empty],
                                       [empty, gr_var_val_1, N_1, n_1, percents_1, ci_low_1, ci_upp_1, stats, p_value],
                                       [empty, gr_var_val_2, N_2, n_2, percents_2, ci_low_2, ci_upp_2, stats, p_value]):
                values_sample_t.append(v_t)
                values_sample_1.append(v_1)
                values_sample_2.append(v_2)
            rows_num = df_out.shape[0]
            for row in [values_sample_t,
                        values_sample_1,
                        values_sample_2]:
                df_out.loc[rows_num] = row
                rows_num +=1

            # print(df_out)
            # print(f"Общая выборка по <{column_name}>")
            # print(*values_sample_t, sep="\n")
            # print(f"1-ая выборка для <{gr_var_val_1}>")
            # print(*values_sample_1, sep="\n")
            # print(f"2-ая выборка для <{gr_var_val_2}>")
            # print(*values_sample_2, sep="\n")
        return df_out


if __name__ == '__main__':
    df_test = pd_DataFrame({
        'группа': [1, 0, 1, 0, 1, 1, 0],
        'пол':    [0, 0, 0, 1, 1, 1, 1],
        'ГБ':     [1, 0, 0, 1, 0, '', 0],
        "ИМТ":    [33, 25, 19.8, 25, 22, 3.1, 20],
        "возраст": [19, 22, 20, 21, 51, 65, 79]
    })

    descr_test = Describer(df=df_test)
    res_binar = descr_test.calculate_descr_stats_binar_vars(grouping_variable_name='группа',
                                                      analyzed_variable_names=['пол', 'ГБ'],
                                                      colnames_lang="EN")
    # print(res_binar)
    res_quantit = descr_test.compute_quantitative_variables(grouping_variable_name='группа',
                                                            quantitative_variable_names=['ИМТ', 'возраст'],
                                                            colnames_lang="EN")
    print(res_quantit)
    res_binar.to_excel("test_binary_vars_processing.xlsx")
    res_quantit.to_excel("test_quantit_vars_processing.xlsx")
