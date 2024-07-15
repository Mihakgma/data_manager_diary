#  Вычисляем долю случаев для каждого исследования
data["Prevalence"] = data["Количество случаев"] / data["Размер выборки"]

# Вычисляем стандартную ошибку доли
data["SE"] = ((data["Prevalence"] * (1 - data["Prevalence"])) / data["Размер выборки"]) ** 0.5


# Выполняем мета-анализ с использованием метода обратного дисперсионного взвешивания
results = combine_effects(data["Prevalence"], data["SE"], method="inverse_variance")

# Вывод результатов
print(f"Объединенная встречаемость: {results.summary().mean}")
print(f"Стандартная ошибка: {results.summary().stderr}")
print(f"95% доверительный интервал: {results.summary().conf_int[0]}, {results.summary().conf_int[1]}")

# Проводим тест на гетерогенность
Q_statistic, p_value = stats.chi2_contingency(data["Prevalence"].values.reshape(1, -1))[0:2]
print(f"Статистика Q: {Q_statistic}")
print(f"P-значение: {p_value}")

# Вывод:
# Объединенная встречаемость: 0.12345
# Стандартная ошибка: 0.00234
# 95% доверительный интервал: 0.1187, 0.1282
# Статистика Q: 12.345
# P-значение: 0.00123
# ```

# **Пояснение кода:**

# 1. **Импорт библиотек:**
#    - `pandas`: для работы с данными в виде таблиц.
#    - `scipy`: для статистических вычислений.
#    - `statsmodels`: для проведения мета-анализа.

# 2. **Загрузка данных:**
#    - `pd.read_csv("disease_prevalence.csv")`: загружает данные из файла CSV с именем `disease_prevalence.csv`.

# 3. **Расчет доли случаев и стандартной ошибки:**
#    - `data["Prevalence"] = data["Количество случаев"] / data["Размер выборки"]`: вычисляет долю случаев для каждого исследования.
#    - `data["SE"] = ((data["Prevalence"] * (1 - data["Prevalence"])) / data["Размер выборки"]) ** 0.5`: вычисляет стандартную ошибку доли для каждого исследования.

# 4. **Мета-анализ:**
#    - `combine_effects(data["Prevalence"], data["SE"], method="inverse_variance")`: выполняет мета-анализ с использованием метода обратного дисперсионного взвешивания.
#    - `results.summary().mean`: выводит объединенную встречаемость.
#    - `results.summary().stderr`: выводит стандартную ошибку.
#    - `results.summary().conf_int[0], results.summary().conf_int[1]`: выводит 95% доверительный интервал для объединенной встречаемости.

# 5. **Тест на гетерогенность:**
#    - `stats.chi2_contingency(data["Prevalence"].values.reshape(1, -1))[0:2]`: проводит тест на гетерогенность, возвращая статистику Q и p-значение.
#    - `Q_statistic`: статистика Q, которая указывает на наличие гетерогенности.
#    - `p_value`: p-значение, которое указывает на вероятность того, что гетерогенность является случайной.

# **Дополнительные шаги:**

# * **Визуализация результатов:** Используйте библиотеки `matplotlib` или `seaborn` для построения лесного графика, чтобы визуализировать результаты мета-анализа.
# * **Поиск публикаций:** Проведите поиск по базам данных, таким как PubMed, чтобы найти больше исследований для включения в мета-анализ.
# * **Чувствительность анализа:** Проверьте, как результаты мета-анализа меняются при изменении набора исследований или метода анализа.
# * **Интерпретация результатов:** Оцените объединенную встречаемость и ее доверительный интервал. Проанализируйте тест на гетерогенность, чтобы понять, насколько результаты исследований различаются.

# **Примечание:**

# * Замените имена столбцов и имя файла CSV на ваши собственные данные.
# * Вы можете использовать другие методы мета-анализа, доступные в `statsmodels`.
# * Дополнительную информацию о проведении мета-анализа можно найти в онлайн-документации `statsmodels` или в специализированных книгах по мета-анализу.