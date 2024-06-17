# chi-squared test with similar proportions
from scipy.stats import chi2_contingency
from scipy.stats import chi2
# Критерий Фишера
from scipy.stats import fisher_exact
from numpy import nan as np_nan
# CIs for proportions
from statsmodels.stats.proportion import proportion_confint
from datetime import datetime as datetime_dt


INDEPENDENT_SAMPLES = '\nIndependent of Grouping Factor (p-value >= 0.05 -> fail to reject H0)\n'
DEPENDENT_SAMPLES = '\nDependent of Grouping Factor (p-value < 0.05 -> reject H0)\n'


def chi_squaredtest(table):
    stat, p, dof, expected = chi2_contingency(table)
    out_str = ""
    s = 'dof=%d\n' % dof
    out_str += s
    print(out_str)
    # print(expected)
    # interpret test-statistic
    prob = 0.95
    critical = chi2.ppf(prob, dof)
    s = 'probability=%.3f, critical=%.3f, stat=%.3f\n' % (prob, critical, stat)
    print(s)
    out_str += s
    if abs(stat) >= critical:
        s = DEPENDENT_SAMPLES
        out_str += s
        print(s)
    else:
        s = INDEPENDENT_SAMPLES
        out_str += s
        print(s)
    # interpret p-value
    alpha = 1.0 - prob
    s = 'significance=%.3f, p=%.3f' % (alpha, p)
    out_str += s
    print(s)
    if p <= alpha:
        s = DEPENDENT_SAMPLES
        out_str += s
        print(s)
    else:
        s = INDEPENDENT_SAMPLES
        out_str += s
        print(s)

    return stat, p, dof, expected, out_str


def chisq_fisher_tests(lst1: list, lst2:list):
    pity_frequency = False
    curr_stats = '-'
    curr_p_value = '-'
    black_list = ['', 0, np_nan]
    used_method = ""
    detailed_info = ""

    # print(lst1)
    # print(lst2)

    if any([i in lst1 for i in black_list]) or any([i in lst2 for i in black_list]):
        return curr_stats, curr_p_value
    if len(lst1) != len(lst2) != 2:
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
            used_method = "An error occurred:\n"
        #fisher_exact возвращает 2 переменные - oddsr, p
        curr_stats = '-'
        curr_p_value = round(fisher[1], 3)
        used_method = "Fishers exact test:\n"
        detailed_info = DEPENDENT_SAMPLES if curr_p_value <= 0.05 else INDEPENDENT_SAMPLES

    elif not(pity_frequency):
        xi_square_results = chi_squaredtest(curr_cont_table)
        #print('Хи-Квадрат посчитан')
        curr_stats = round(xi_square_results[0], 2)
        curr_p_value = round(xi_square_results[1], 5)
        used_method = "Chi-squared test:\n"
        detailed_info = xi_square_results[4]

    return used_method, detailed_info, curr_stats, curr_p_value


def count_conf_int(n:int,
                   N:int,
                   replace_dot_comma=True):
    """
    Расчет 95% ДИ для доли.
    n - частота встречаемости признака в группе
    N - общее количество наблюдений в выборке
    принтует результат в руссоком формате -
    вместо . в качестве разделителя десятичн дробей - ,
    """
    ci_low, ci_upp = proportion_confint(count=n,
                                        nobs=N,
                                        alpha=0.05,
                                        method='normal')
    ci_low = round(ci_low * 100, 2)
    ci_upp = round(ci_upp * 100, 2)
    percents = round((n * 100) / N, 2)
    result = f'{percents} [{ci_low}–{ci_upp}] %'
    if replace_dot_comma:
        result = result.replace('.', ',')
    return {"percents": percents, "ci_low": ci_low, "ci_upp": ci_upp, "result_str": result}


class BinarStatsCalc:
    __GROUPS_NUMBER_DEFAULT = 2
    __MAX_GROUPS_NUMBER = 20
    __TRIES_NUMBER = 3
    __MIN_ABS_FREQENCY = 1
    __MAX_ABS_FREQENCY = 10000
    __RESULTS_FILE_NAME = "descriptive_stats_results.txt"
    __DOCS_FILE_NAME = "descriptive_stats_documentation.txt"
    __MENU_TEXT = ["1 - VIEW DOCUMENTATION",
                   "2 - START COMPUTING"]
    __INPUT_ERROR_WARNING = "INPUT ERROR!!! PLEASE, RETRY..."

    def __init__(self):
        self.__groups_number = self.__GROUPS_NUMBER_DEFAULT

    def get_groups_number(self):
        return self.__groups_number

    def set_groups_number(self, groups_number):
        self.__groups_number = groups_number


    def calculate(self, groups_number):
        # self.groups_number = self.process_integer_inputted("Пожалуйста, введите количество групп сравнения:\n")
        # groups_number = self.get_groups_number()
        data_list = []
        out_list = []
        for i in range(groups_number):
            txt = "\n---///---\n"
            txt += f'<{i + 1}> группа:\n'
            print(txt)
            N = self.__process_integer_inputted(
                "Пожалуйста, введите (N) общее количество наблюдений в текущей группе:\n")
            n = self.__process_integer_inputted("Пожалуйста, введите (n) количество " +
                                                "наблюдений с наличием признака:\n", N)
            k = N - n
            # print(k)
            ci_results = count_conf_int(n, N)
            # print(ci_results)
            txt += f"N = <{N}>, n = <{n}>\n"
            ci_str = ci_results["result_str"]
            txt += f"<{ci_str}>"
            # print(txt)
            out_list.append(txt)
            data_list.append([n, k])
        if len(data_list) == 2:
            test_result = chisq_fisher_tests(lst1=data_list[0],
                                             lst2=data_list[1])
        # print(test_result)
        out_list.append("\n".join([str(i) for i in list(test_result)]))
        # print(*out_list)
        print(f"Длина листа с результатами: {len(out_list)}")
        print(*out_list, sep="\n")
        return out_list


    def __print_input_error(self, max_value):
        # if max_value == -999:
        #     max_value = self.__MAX_ABS_FREQENCY
        print("Вводимое значение должно быть в интервале")
        print(f"ОТ <{self.__MIN_ABS_FREQENCY}> и ДО <{max_value}> (не включ.)")

    def __invoke_application_fail(self):
        print("Работа программы завершена.")
        input("Для выхода нажмите Enter...")
        raise TypeError

    def __process_integer_inputted(self, text: str, max_freq=-999):
        if max_freq == -999:
            max_freq = self.__MAX_ABS_FREQENCY
        i = 0
        while i < self.__TRIES_NUMBER:
            i += 1
            answer = input(text)
            try:
                digit_inputted = int(answer)
                if max_freq >= digit_inputted >= self.__MIN_ABS_FREQENCY:
                    return digit_inputted
                else:
                    self.__print_input_error(max_freq)
            except TypeError:
                self.__print_input_error(max_value=max_freq)
            except ValueError:
                self.__print_input_error(max_value=max_freq)
        self.__invoke_application_fail()

    @staticmethod
    def write_lines_to_file(file_path, lines):
        """
          Writes lines to a text file, creating the file if it doesn't exist.

          Args:
              file_path (str): The path to the text file.
              lines (list): A list of strings to write to the file.
        """

        with open(file_path, 'a+', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        print(f"Results has been added to a file: <{file_path}>")

    def get_current_time_string(self):
        """Возвращает текущее время в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС в виде строки."""
        now = datetime_dt.now()
        return now.strftime("%d.%m.%Y %H:%M:%S")


    def init_main_menu(self):
        i = 0
        menu_text = self.__MENU_TEXT
        max_menu_value = len(menu_text)
        while i < self.__TRIES_NUMBER:
            i += 1
            answer = input("\n".join(menu_text) + "\n")
            if not any(answer in i for i in menu_text):
                print(self.__INPUT_ERROR_WARNING)
                pass
            try:
                digit_inputted = int(answer)
                # if max_menu_value >= digit_inputted >= self.__MIN_ABS_FREQENCY:
                if digit_inputted == 1:
                    docs = BinarStatsCalc.get_docs()
                    print(docs)
                    break
                elif digit_inputted == 2:
                    results = self.calculate(groups_number=self.get_groups_number())
                    # print(results)
                    res = ["\n"*2, self.get_current_time_string()]
                    res += results
                    BinarStatsCalc.write_lines_to_file(file_path=self.__RESULTS_FILE_NAME,
                                                       lines=res)
                    break
                else:
                    self.__print_input_error(max_menu_value)
            except TypeError as e:
                print("TypeError")
                print(e)
                self.__print_input_error(max_value=max_menu_value)
            except ValueError as e:
                print("ValueError")
                print(e)
                self.__print_input_error(max_value=max_menu_value)
        # self.__invoke_application_fail()

    @staticmethod
    def get_docs():
        txt = f"""
        Program documentations & instructions
        
        Данная программа предназначена для расчета процентов и их 95%-ых
        доверительных интервалов (ДИ), а также значимости различий между выборками.
        Для оценки статистической значимости качественных признаков использовали анализ таблиц сопряженности 
        (четырехпольная таблица) – критерий χ2-Пирсона.
        В случае, когда одно из ожидаемых значений составляет от 5 до 9, критерий χ2 рассчитывался с поправкой Йейтса. 
        При частотах меньше 5 применялся точный метод Фишера. При использовании точного метода Фишера значение, 
        полученное в ходе расчета критерия, соответствует точному значению уровня значимости р. 
        Результаты расчетов нижней и верхней границ 95%-ого доверительного интервала для доли, 
        выраженной в процентах (%) представлены в следующем виде:

        Расшифровки:
        N - общее количество наблюдений в текущей группе;
        n - количество наблюдений с наличием признака;
        dof - количество степеней свободы (Degrees of Freedom);
        fail to reject H0 - НЕВОЗМОЖНО отклонить нулевую гипотезу об отсутствии влияния группирующего фактора 
                            на частоту встречаемости изучаемого признака (p-value >= 0,05);
        (reject H0) - ОТКЛОНЯЕМ нулевую гипотезу об отсутствии влияния группирующего фактора 
                      на частоту встречаемости изучаемого признака (p-value < 0,05).
        
        Результаты не только выводятся в консоль, но также сохраняются 
        в рабочей директории (папка с программой) в текстовый файл с
        названием <{BinarStatsCalc.__RESULTS_FILE_NAME}>
        
        ИСТОЧНИКИ:
        О.В. Иванов «Статистика. Учебный курс для социологов и менеджеров. Часть 2» Москва, 2005. 220 с. (стр. 15–17).
        """
        return txt


if __name__ == '__main__':
    # lst_1 = [5, 10]
    # lst_2 = [3, 99]
    # res = chisq_fisher_tests(lst1=lst_1,
    #                          lst2=lst_2)
    # print(res)
    #
    # res = count_conf_int(n=50, N=100)
    # print(res)
    calc = BinarStatsCalc()
    calc.init_main_menu()
    input("Для выхода нажмите Enter...")
