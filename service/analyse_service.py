import logging
import pandas as pd


logger = logging.getLogger(__name__)

# пропущенные значения
def _count_of_missing_value(data: pd.DataFrame) -> pd.Series:
    return data.isna().sum()

def find_outliers_iqr_dict(df, columns) -> dict[str, list[int]]:
    outliers_dict = {}  # Словарь для хранения выбросов по каждому столбцу
    for col in columns:
        # Вычисляем Q1, Q3 и IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Вычисляем границы для выбросов
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Фильтруем выбросы: значения меньше нижней границы или больше верхней
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].tolist()
        
        # Добавляем в словарь, если есть выбросы
        if outliers:
            outliers_dict[col] = outliers
            
    return outliers_dict


# выбросы 
def _count_of_outliers(data: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = data.select_dtypes(include=['number']).columns

    outliers_dict = find_outliers_iqr_dict(data, numeric_columns)

    outliers_list = []

    for col, outliers in outliers_dict.items():
        outliers_list.append([col, outliers])

    outliers_df = pd.DataFrame(outliers_list, columns=['Столбец', 'Выбросы'])

    return outliers_df


# статистическая информация
def _stat_info(data: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = data.select_dtypes(include=['number']).columns

    # среднее
    mean_data = data[numeric_columns].mean().dropna()
    mean_df = mean_data.reset_index()
    mean_df.columns = ['Столбец', 'Среднее']

    # медиана
    median_data = data[numeric_columns].median().dropna()
    median_df = median_data.reset_index()
    median_df.columns = ['Столбец', 'Медиана']

    # минимальное значение
    min_data = data[numeric_columns].min().dropna()
    min_df = min_data.reset_index()
    min_df.columns = ['Столбец', 'Минимум']

    # максимальное значение
    max_data = data[numeric_columns].max().dropna()
    max_df = max_data.reset_index()
    max_df.columns = ['Столбец', 'Максимум']

    res_df = mean_df.merge(median_df, how='inner', on='Столбец')
    res_df = res_df.merge(max_df, how='inner', on='Столбец')
    res_df = res_df.merge(min_df, how='inner', on='Столбец')

    return res_df


def _write_df(writer: pd.ExcelWriter, df: pd.DataFrame, sheetname: str, header: str = 'Информация по данным'):
    df.to_excel(writer, sheet_name=sheetname, header=False, index=False, startrow=3, startcol=0)

    wb = writer.book
    worksheet = wb[sheetname]

    worksheet['A2'] = header

    for col in worksheet.columns:
        worksheet.column_dimensions[col[0].column_letter].auto_size = True


def save_result_file(path: str, file_id: str):
    logger.info(f'Proccessing file: {path}')

    data = pd.read_excel(path, engine='openpyxl')

    missing_value_df = _count_of_missing_value(data)
    stat_df = _stat_info(data)
    outliers_df = _count_of_outliers(data)

    file_path = './files_out/result_' + file_id + '.xlsx'

    writer = pd.ExcelWriter(file_path, engine='openpyxl')

    _write_df(writer, missing_value_df, 'missing_value', 'Таблица пропущенных значений')
    _write_df(writer, stat_df, 'stat', 'Статистика по данным')
    _write_df(writer, outliers_df, 'outliers', 'Статистика по выбросам вычисленным с помощью IQR')

    writer.close()

    return file_path