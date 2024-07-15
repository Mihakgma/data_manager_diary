# from meta_analysis import MetaAnalysis
from data_processing import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    preprocess_data(excel_file_fullpath=filename, research_object_mark_colname=research_object_mark_colname,
                    research_object_mark=research_object_mark, variables_lst=variables_lst,
                    publication_colname=colnames_lst[0], colnames_lst=colnames_lst,
                    researches_number=researches_number, only_current_research=only_current_research,
                    current_resch_mark=current_resch_mark,
                    group_colname=group_colname, group_values_filter=group_values_filter)
    # meta_a = MetaAnalysis({}, "", "")
    # meta_a.RESULT_COLNAMES
