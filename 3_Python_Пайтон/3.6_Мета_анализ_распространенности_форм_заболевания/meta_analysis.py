from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects
# работа с таблицами
import pandas as pd
# import matplotlib.pyplot as plt


class MetaAnalysis:
    VALUE_DEFAULT = "-"
    PRVLNC_STR = "Prevalence"
    COMBINE_EFFECTS_METHOD = "iterated"
    SUMM_FRAME_ROW_NUMBER = -4
    ROUND_RESULTS_DIGITS = 5
    RESULT_COLNAMES = [
        "overall_prevalence",
        "se",
        "ci_lower",
        "ci_upper",
        "Q_statistic",
        "p_value"
    ]

    def __init__(self,
                 data: pd.DataFrame,
                 n: str,
                 N: str):
        # нужно сохранить индекс ДФ для итоговой таблицы!!!
        # self.data = data.reset_index()
        self.data = data
        self.n = n
        self.N = N
        self.results = {}
        # заполняем словарь значениями по умолчанию
        [self.results.update({k: MetaAnalysis.VALUE_DEFAULT})
         for k in MetaAnalysis.RESULT_COLNAMES]
        self.summary_results = None
        self.summary_frame = None

    @staticmethod
    def get_result_names():
        pass

    def get_combined_results(self):
        df = pd.DataFrame(self.summary_frame)
        Q_str = self.RESULT_COLNAMES[4]
        p_value_str = self.RESULT_COLNAMES[5]
        Q, p = self.results[Q_str], self.results[p_value_str]
        extend_elements_on = df.shape[1] - 1
        lst = []
        lst.append(Q)
        df.loc[Q_str] = lst + [self.VALUE_DEFAULT] * extend_elements_on
        lst = []
        lst.append(p)
        df.loc[p_value_str] = lst + [self.VALUE_DEFAULT] * extend_elements_on
        return df

    def updt_results(self, results: list):
        for k, v in zip(list(self.results), results):
            self.results[k] = v

    def calculate_meta_analysis(self):
        overall_prevalence, se, ci_lower, ci_upper, Q_statistic, p_value = [self.VALUE_DEFAULT] * len(
            self.RESULT_COLNAMES)
        data = self.data
        n = self.n
        N = self.N

        # try:
        #  Вычисляем долю случаев для каждого исследования
        data[self.PRVLNC_STR] = data[n] / data[N]

        # Вычисляем стандартную ошибку доли
        data["SE"] = ((data[self.PRVLNC_STR] * (1 - data[self.PRVLNC_STR])) / data[N]) ** 0.5
        index_values = list(data.index.values)
        # print(index_values)
        # Выполняем мета-анализ с использованием метода обратного дисперсионного взвешивания
        results = combine_effects(data[self.PRVLNC_STR],
                                  data["SE"],
                                  row_names=index_values,
                                  method_re=self.COMBINE_EFFECTS_METHOD)
        self.summary_results = results
        # print(results.conf_int_samples())
        res = results.summary_frame().iloc[data.shape[0], :]
        # print(results.cache_ci)
        # print(results.summary_frame())
        # print(results.summary_frame().index)
        self.summary_frame = results.summary_frame()
        # self.save_fig()
        # input()
        # print(type(results))
        overall_prevalence = res["eff"]
        se = res["sd_eff"]
        ci_lower = res["ci_low"]
        ci_upper = res["ci_upp"]
        # Вывод результатов
        # print(f"Объединенная встречаемость: {overall_prevalence}")
        # print(f"Стандартная ошибка: {se}")
        # print(f"95% доверительный интервал: {ci_lower}, {ci_upper}")

        # Проводим тест на гетерогенность
        # reshaped_data = data[self.PRVLNC_STR].values.reshape(1, -1)
        # print(reshaped_data)
        # Q_statistic, p_value = stats.chi2_contingency(reshaped_data)[0:2]

        absolute_frequencies = [
            data[n].tolist(),
            data[N].tolist()
        ]
        # print(absolute_frequencies)
        Q_statistic, p_value = stats.chi2_contingency(absolute_frequencies)[0:2]
        # print(f"Статистика Q: {Q_statistic}")
        # print(f"P-значение: {p_value}")
        # except Exception as e:
        #   print(e)
        self.updt_results(results=[round(i, self.ROUND_RESULTS_DIGITS) for i in
                                   [overall_prevalence, se, ci_lower, ci_upper, Q_statistic, p_value]])
        return results

    def save_fig(self,
                 full_path_filename: str = "test.png",
                 figheight: int = 6,
                 figwidth: int = 6):
        info = self.summary_results
        fig = info.plot_forest()
        fig.set_figheight(figheight)
        fig.set_figwidth(figwidth)
        # fig.draw()
        # fig.show()
        try:
            fig.savefig("."+full_path_filename,
                    dpi=500, facecolor='w', edgecolor='w', orientation='portrait',
                    papertype=None, format=None, pad_inches=0.1, bbox_inches='tight')
        except FileNotFoundError:
            fig.savefig(full_path_filename,
                        dpi=500, facecolor='w', edgecolor='w', orientation='portrait',
                        papertype=None, format=None, pad_inches=0.1, bbox_inches='tight')


if __name__ == '__main__':
    reserches_lst = [
        "Исследование №1",
        "Исследование №2",
        "Исследование №3",
        "Исследование №4",
        "Исследование №5",
    ]
    df_test = pd.DataFrame({
        "исследования": reserches_lst,
        "A": [200, 11, 77, 33, 99],
        "a": [110, 3, 25, 21, 11],
        "B": [19, 0, 0, 0, 0],
        "b": [12, 0, 0, 0, 0],
        "C": [170, 0, 0, 0, 0],
        "c": [33, 0, 0, 0, 0],
    })

    df_test.set_index("исследования",
                      inplace=True,
                      drop=True)
    # print(df_test.index.values)
    # print(df_test)
    meta_a = MetaAnalysis(df_test, n="a", N="A")
    print(meta_a.RESULT_COLNAMES)
    meta_a.calculate_meta_analysis()
    print(*[(k, v) for (k, v) in meta_a.results.items()], sep="\n")
    print(meta_a.get_combined_results())
