import pandas as pd


def excel_to_data_frame_parser(file:str,
                               page_number:int=1):

    """
    Парсит эксель-файл с выбором листа.
    Возвращает датафрейм (далее - ДФ).
    """

    try:
        file = file

    except BaseException:
        print("Ошибка ввода")
        input()
    data = pd.ExcelFile(file)
    my_sheet_names = data.sheet_names
    print("Названия листов в книге: ")
    print(my_sheet_names)
    nomer_lista = page_number - 1
    df = data.parse(my_sheet_names[nomer_lista])
    print(f'Размерность ДФ: <{df.shape}>')
    print('OK!')
    #input()

    return df

def printDimensionsOfDF(dfInput: pd.DataFrame, warnStr:str=''):
    dfDimsLst = dfInput.shape
    print('После <'+warnStr+'>')
    print(f"""размерность ДФ составила:
    <{dfDimsLst[0]}> строк на <{dfDimsLst[1]}> столбцов""")
