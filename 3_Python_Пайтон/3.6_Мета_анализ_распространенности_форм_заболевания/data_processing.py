# Импорт своих модулей
import numpy as np

from parse_excel_df import excel_to_data_frame_parser, printDimensionsOfDF
from get_pairs import get_all_pairs
from df_processor import df_process
from df_to_excel import SaveDataFrames


def transform_str(text: str):
    if type(text) != str:
        raise TypeError(f"Cannot transform object of <{type(text)}> type!!!")
    return text.strip().lower()


def preprocess_data(excel_file_fullpath: str,
                 research_object_mark_colname:str,
                 research_object_mark:str,
                 variables_lst: list,
                 publication_colname:str,
                 colnames_lst: list,
                 researches_number:int,
                 only_current_research: bool,
                 current_resch_mark: str,
                 group_colname: str,
                 group_values_filter: list,
                 img_files_format: str = ".png",
                 need_filter_by_group: bool = True):
    df = excel_to_data_frame_parser(filename)
    # printDimensionsOfDF(df, "первичной подгрузки")
    # print(df.head())
    df_filtered = df[df[research_object_mark_colname] == research_object_mark].dropna(axis=0)
    if need_filter_by_group:
        group_filter_mask = df_filtered[group_colname]\
                            .apply(lambda x: 1 if x in group_values_filter else 0)\
                            .to_list()
        # print(group_filter_mask)
        # print(len(group_filter_mask), df_filtered.shape)
        # group_filter_mask = list(map(bool, group_filter_mask))
        group_filter_mask = np.array(group_filter_mask, dtype=bool)
        df_filtered = df_filtered[group_filter_mask].dropna(axis=0)
        # df_filtered = group_values_filter[np.array(group_filter_mask).astype(bool)].dropna(axis=0)
    # df_filtered = df_filtered[df_filtered["Группа исслед-ий (1-свое, 2-красн, 3-синие, 4-прочие)"] != ""]
    printDimensionsOfDF(df_filtered, "фильтрации")
    # print(df_filtered.tail())
    researchs_lst = df_filtered[publication_colname].value_counts().index.to_list()
    # print(researchs_lst)
    print([i in list(df_filtered) for i in variables_lst])
    # Наименование всех в дальнейшем используемых столбцов
    colnames_lst += variables_lst
    print(f"ДФ содержит поданные наименования столбцов :\n<{colnames_lst}>\n?")
    print([i in list(df_filtered) for i in colnames_lst])
    # все пары (количество элементов = 3) исследований
    research_combos = get_all_pairs(researchs_lst, pairs_value=researches_number)
    # если мы хотим обработать строки ДФ содержащие ТОЛЬКО комбинации с текущим исследованием
    if only_current_research:
        current_resch_mark = transform_str(current_resch_mark)
        research_combos = [i for i in research_combos
                           if current_resch_mark in transform_str("".join(i))]
    print("Количество комбинаций сравнений составило:")
    print(len(research_combos))
    dfs, summary_table, total_objs = df_process(reschs_combos=research_combos, df=df_filtered, df_research_colname=publication_colname,
                                                   all_colnames=colnames_lst, N=colnames_lst[1], vars_colnames=variables_lst)
    # print(dfs)
    i = 0
    for combo in dfs:
        # print(combo)
        i += 1
        save_dfs_obj = SaveDataFrames(dfs_dict=dfs[combo], dir_number=i)
        save_dfs_obj.save_excel_file(file_name=f"{i}")
        dir_path = save_dfs_obj.get_results_dir_path()
        # получаем соотв-ый результат мета-анализа, из которого необходимо извлечь
        # рисунок и сохранить его в указанную директорию!!!
        # словарь!!! пройтись по парам ключ-значение!!!
        meta_a_objs = total_objs[combo]
        for variable in meta_a_objs:
            var_obj = meta_a_objs[variable]
            full_file_path = dir_path + variable + img_files_format
            var_obj.save_fig(full_path_filename=full_file_path)


    # print(summary_table.head(35))
    # print(summary_table.tail(15))
    summary_table.to_excel("test_summary_df.xlsx")
    # print(*[(k, v) for (k, v) in dfs.items()], sep="\n")


filename = r"D:\К\Садовникова Наталья\2024\6-июнь-2024\МЕТА-АНАЛИЗ\ИСХОДНИКИ\мета-анализ таблица.xlsx"
research_object_mark_colname = "Глаза-пациенты"
research_object_mark = "П"
variables_lst = [
    "ПВГ",
    "ЮОУГ",
    "ВГ – Аном",
    "ВГ-Сист",
    "ВГ-Приоб",
    "ВГ-Кат"
]
colnames_lst = [
    "Наименование",
    "Кол-во пациентов/ глаз"
]
only_current_research = True
# количество исследований в одном сравнении (комбинации исследований)
researches_number = 6
current_resch_mark = "Данное исследование"
group_colname = "Группа исслед-ий (1-свое, 2-красн, 3-синие, 4-прочие)"
group_values_filter = [1, 4]


if __name__ == '__main__':
    preprocess_data(excel_file_fullpath=filename, research_object_mark_colname=research_object_mark_colname,
                    research_object_mark=research_object_mark, variables_lst=variables_lst,
                    publication_colname=colnames_lst[0], colnames_lst=colnames_lst,
                    researches_number=researches_number, only_current_research=only_current_research,
                    current_resch_mark=current_resch_mark,
                    group_colname=group_colname, group_values_filter=group_values_filter)
