import pandas as pd
from meta_analysis import MetaAnalysis


def get_meta_results(reschs_combos: list,
                     df: pd.DataFrame,
                     df_research_colname: str,
                     all_colnames: list,
                     N: str,
                     vars_colnames: list,
                     researches_combos_colname: str = "Сравниваемые исследования"):

  """
  НЕОБХОДИМО ИЗМЕНИТЬ ДАННУЮ ФУНКЦИЮ:
  для прохода по всем поданным комбинациям исследований
  сохранения результатов (сводные таблицы мета-анализа)
  в отдельные файлы -> по каждому показателю отдельный лист файла (текущей книги)
  также графики должны быть сохранены специально отведенную директорию:
  графики -> текущая дата + время (ДДММГГГГ_ЧЧММСС) ->
  имя файла(комбинация исследований (порядковый номер из сводного листа ???))
  ТОГДА НУЖЕН СВОДНЫЙ ЛИСТ (экселевский файл, в той же директории с графиками) -эскелевский файл!!!
  :param reschs_combos: комбинация исследований
  :param df: поданный Дата Фрейм пандас
  :param df_research_colname: наименование колонки поданного ДФ с названием исследования
  :param all_colnames: наименования всех колонок поданного ДФ, участвующих в обработке данных
  :param N: общее количество наблюдений (наименование колонки поданного ДФ)
  :param vars_colnames: изучаемые характеристики для проведения мета-анализа (наименование колонок поданн. ДФ)
  :param researches_combos_colname: наименование колонки с исследованиями (для переименования - на выход)
  :return:
  """

  # resch_name_lst = df[df_research_colname].to_list()
  # print(resch_name_lst)
  # print(df.dtypes)
  # df.drop_index(inplace=True)
  meta_a = MetaAnalysis({}, "", "")
  statistics_var_names = list(meta_a.RESULT_COLNAMES)
  df_out = pd.DataFrame({})
  row_first_values = []
  row_first_values.append(researches_combos_colname)
  for variable_colname in vars_colnames:
    # df_out[variable_colname] = {}
    for stats_colname in statistics_var_names:
      df_out[variable_colname + "_" + stats_colname] = []
      # row_first_values.append(variable_colname) # РАСКОММЕНТИТЬ!!!
  row_number = 0
  # df_out.loc[row_number] = row_first_values # РАСКОММЕНТИТЬ!!!
  # df_out = pd.concat(df_out, axis=1)
  # df_out[researches_combos_colname] = reschs_combos
  df_out.insert(0, researches_combos_colname, reschs_combos)
  # print(df_out)
  print(df_out.dtypes)
  for reschs_combo in reschs_combos:
    row_number += 1
    df_marks = []
    for row in df[df_research_colname]:
      df_marks.append(row in reschs_combo)

    df_curr = df[all_colnames][df_marks]
    # df_curr = df_curr
    # print(df_curr.shape)
    vars_results_dict = {}
    row_values = []
    row_values.append("".join(list(reschs_combo)))
    for var in vars_colnames:
      meta_a = MetaAnalysis(data=df_curr, n=var, N=N)
      result_values = [v for (k, v) in meta_a.results.items()]
      vars_results_dict[var] = result_values
      row_values.extend(result_values)
    print(row_values)
    print(len(row_values))
    df_out.loc[row_number] = row_values
  return df_out
