import logging
import pandas as pd

from service.package_service import get_out_file_path

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
    return data.describe()


# матрица корреляции
def _corr_info(data: pd.DataFrame):
    numeric_columns = numeric_columns = data.select_dtypes(include=['number']).columns
    data = data[numeric_columns]
    return data.corr()


def _write_df(writer: pd.ExcelWriter, df: pd.DataFrame, sheetname: str, header: str = 'Информация по данным'):
    df.to_excel(writer, sheet_name=sheetname, header=True, index=True, startrow=3, startcol=0)

    wb = writer.book
    worksheet = wb[sheetname]

    worksheet['A2'] = header

    for col in worksheet.columns:
        worksheet.column_dimensions[col[0].column_letter].auto_size = True


def missing_values_file_save(column: str, file_id: str, path: str):
    logger.info(f'Proccessing file: {path}')

    data = pd.read_excel(path, engine='openpyxl')
    missing_value_df = _count_of_missing_value(data[[column]])

    file_path = get_out_file_path(file_id)

    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    file_path = get_out_file_path(file_id)
    _write_df(writer, missing_value_df, 'missing_value', 'Таблица пропущенных значений')
    writer.close()

    return file_path


def get_stat_file_save(column: str, file_id: str, path: str):
    logger.info(f'Proccessing file: {path}')

    data = pd.read_excel(path, engine='openpyxl')
    stat_df = _stat_info(data[[column]])

    file_path = get_out_file_path(file_id)

    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    file_path = get_out_file_path(file_id)
    _write_df(writer, stat_df, 'get_stat', 'Статистика по столбцу')
    writer.close()

    return file_path


def get_outliers_file_save(column: str, file_id: str, path: str):
    logger.info(f'Proccessing file: {path}')

    data = pd.read_excel(path, engine='openpyxl')
    outliers_df = _count_of_outliers(data[[column]])

    file_path = get_out_file_path(file_id)

    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    file_path = get_out_file_path(file_id)
    _write_df(writer, outliers_df, 'outliers', 'Статистика по выбросам')
    writer.close()

    return file_path



def save_result_file(path: str, file_id: str) -> str:
    logger.info(f'Proccessing file: {path}')

    data = pd.read_excel(path, engine='openpyxl')

    missing_value_df = _count_of_missing_value(data)
    stat_df = _stat_info(data)
    outliers_df = _count_of_outliers(data)
    corr_df = _corr_info(data)

    file_path = get_out_file_path(file_id)

    writer = pd.ExcelWriter(file_path, engine='openpyxl')

    _write_df(writer, missing_value_df, 'missing_value', 'Таблица пропущенных значений')
    _write_df(writer, stat_df, 'stat', 'Статистика по данным')
    _write_df(writer, outliers_df, 'outliers', 'Статистика по выбросам вычисленным с помощью IQR')
    _write_df(writer, corr_df, 'corr', 'Коэффициенты корреляции')

    writer.close()

    return file_path


def get_columns(path: str):
    logger.info(f'Proccessing file: {path}')
    data = pd.read_excel(path, engine='openpyxl')
    return data.columns