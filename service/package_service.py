import os
import logging

logger = logging.getLogger(__name__)

in_dir_name = 'files_in'
out_dir_name = 'files_out'

in_file_prefix = "file_"
out_file_prefix = 'result_'

def get_in_file_path(file_id: str) -> str:
    if not os.path.exists(in_dir_name):
        os.mkdir(in_dir_name)
    
    return os.path.join('.', in_dir_name, in_file_prefix + file_id + '.xlsx')

def get_out_file_path(file_id: str) -> str:
    if not os.path.exists(out_dir_name):
        os.mkdir(out_dir_name)

    return os.path.join('.', out_dir_name, out_file_prefix + file_id + '.xlsx')
    

def delete_files():
    logging.info(f'Deleting files in {in_dir_name}, {out_dir_name}')
    _delete_file_in_path(in_dir_name)
    _delete_file_in_path(out_dir_name)


def _delete_file_in_path(folder_path: str):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.warning(f'Ошибка при удалении файла {file_path}. {e}')