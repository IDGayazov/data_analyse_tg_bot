LEXICON_RU = {
    '/start':   'Приветствую! \n'
                'Я телеграмм бот для анализа данных \n'
                'Введите команду /help для того, чтобы узнать о моих возможностях.',
    '/help':    'Введите команды: \n'
                '/fullan - полный анализ всей таблицы \n'
                '/partan - анализ для признака таблицы \n'
                'Бот может выполнять следующие задачи: \n'
                '- Посчитать количество пропущенных значений;\n'
                '- Проанализировать выбросы для каждого столбца (интерквартильная широта);\n'
                '- Найти выборочные среднее, медиану и дисперсию;\n'
                '- Вывести таблицу корреляции для признаков;\n'
                'Результаты будут выведены в виде файла xlsx.',
    '/fullan':  'Введите файл в формате xlsx',
    '/partan':  'Введите файл в формате xlsx',
    'choose_column': 'Выберите столбец:',
    'choose_action': 'Выберите действие: ',
    "other_message":  'Я всего лишь бот для анализа данных.\n' 
                      'Введите команду /help, чтобы узнать о моих возможностях.',
    'error_file': 'Введите файл формата xlsx',
    'missing_values': 'Подсчитать число пропущенных значений',
    'get_stat': 'Вывести статистику по столбцу',
    'get_outliers': 'Вывести выбросы по столбцу',
    'get_values': 'Вывести распределение значений по столбцу'
}

LEXICON_KEYBOARD = {
    'forward': '>>',
    'backward': '<<'
}