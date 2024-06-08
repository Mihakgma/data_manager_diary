from tqdm.auto import tqdm
from numpy import mean as np_mean
from numpy import std as np_std
from scipy.stats import norm
import matplotlib.pyplot as plt
from pandas import DataFrame as pd_DataFrame


def get_bootstrap(
        data_column_1,  # числовые значения первой выборки
        data_column_2,  # числовые значения второй выборки
        boot_it=1000,  # количество бутстрэп-подвыборок
        statistic=np_mean,  # интересующая нас статистика
        bootstrap_conf_level=0.95  # уровень значимости
):
    boot_len = max([len(data_column_1), len(data_column_2)])
    boot_data = []
    for i in tqdm(range(boot_it)):  # извлекаем подвыборки
        samples_1 = data_column_1.sample(
            boot_len,
            replace=True  # параметр возвращения
        ).values

        samples_2 = data_column_2.sample(
            boot_len,  # чтобы сохранить дисперсию, берем такой же размер выборки
            replace=True
        ).values

        boot_data.append(statistic(samples_1 - samples_2))
    pd_boot_data = pd_DataFrame(boot_data)

    left_quant = (1 - bootstrap_conf_level) / 2
    right_quant = 1 - (1 - bootstrap_conf_level) / 2
    quants = pd_boot_data.quantile([left_quant, right_quant])

    p_1 = norm.cdf(
        x=0,
        loc=np_mean(boot_data),
        scale=np_std(boot_data)
    )
    p_2 = norm.cdf(
        x=0,
        loc=-np_mean(boot_data),
        scale=np_std(boot_data)
    )
    p_value = min(p_1, p_2) * 2

    # Визуализация
    # _, _, bars = plt.hist(pd_boot_data[0], bins=50)
    # for bar in bars:
    #     if abs(bar.get_x()) <= quants.iloc[0][0] or abs(bar.get_x()) >= quants.iloc[1][0]:
    #         bar.set_facecolor('red')
    #     else:
    #         bar.set_facecolor('grey')
    #         bar.set_edgecolor('black')
    #
    # plt.style.use('ggplot')
    # plt.vlines(quants, ymin=0, ymax=50, linestyle='--')
    # plt.xlabel('boot_data')
    # plt.ylabel('frequency')
    # plt.title("Histogram of boot_data")
    # plt.show()

    return {"boot_data": boot_data,
            "quants": quants,
            "p_value": p_value}


if __name__ == '__main__':
    pass
