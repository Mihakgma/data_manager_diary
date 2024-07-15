import pandas as pd
from meta_analysis import MetaAnalysis


def df_process(reschs_combos: list,
               df: pd.DataFrame,
               df_research_colname: str,
               all_colnames: list,
               N: str,
               vars_colnames: list,
               combos_worksheet_name: str = "Сравниваемые исследования",
               graphs_format: str = ".png"):
    # словарь, содержащий ДФ-ы с результатами
    dfs_dict = {}
    summary_objs_dict = {}
    # ключами в нем являются поданные комбинации исследований
    [dfs_dict.update({combo: {}, }) for combo in reschs_combos]
    [summary_objs_dict.update({combo: {}, }) for combo in reschs_combos]
    # print(*[(k,v) for (k,v) in dfs_dict.items()], sep="\n")
    row_number = 0
    summary_table = pd.DataFrame({combos_worksheet_name: []})
    for variable_label in vars_colnames:
        p_variable_label = f"p_value_{variable_label}"
        summary_table[p_variable_label] = []

    for combo in reschs_combos:
        summary_table_row_values = []
        summary_table_row_values.append(combo)

        df_current_combo = pd.DataFrame({combos_worksheet_name: combo})
        dfs_dict[combo][combos_worksheet_name] = df_current_combo

        row_number += 1
        df_marks = []
        for row in df[df_research_colname]:
            df_marks.append(row in combo)
        # фильтруем ДФ по названиям исследований из текущей комбинации
        df_curr = df[all_colnames][df_marks].copy()
        # названия исследований из колонки переносим в индекс!
        df_curr.set_index(df_research_colname,
                          inplace=True,
                          drop=True)

        for variable_label in vars_colnames:
            meta_a = MetaAnalysis(df_curr, n=variable_label, N=N)
            # print(meta_a.RESULT_COLNAMES)
            meta_a.calculate_meta_analysis()
            # print(*[(k, v) for (k, v) in meta_a.results.items()], sep="\n")
            result_frame = meta_a.get_combined_results()
            dfs_dict[combo][variable_label] = result_frame
            summary_objs_dict[combo][variable_label] = meta_a
            summary_table_row_values.append(meta_a.results["p_value"])
            # СОХРАНЕНИЕ ПОЛУЧЕННЫХ РИСУНКОВ!!! - НЕ ЗДЕСЬ!!!
            # graph_file_name = f"{row_number}_"
            # print()
        summary_table.loc[row_number] = summary_table_row_values
    return dfs_dict, summary_table, summary_objs_dict
