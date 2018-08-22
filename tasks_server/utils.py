import os


def _does_file_exist_in_dir(path, files):
    files_not_exist = []
    for file in files:
        if not os.path.isfile(os.path.join(path, file)):
            files_not_exist.append(file)
    return files_not_exist


def check_dir_exist(func):
    def wrapper(*args, **kwargs):
        error_msg = None
        dist_path = args[0].dist_path
        source_path = args[0].source_path
        files_for_check = args[0].files_for_check
        files_not_exist = _does_file_exist_in_dir(source_path, files_for_check)
        if files_not_exist:
            error_msg = "This files '{}' not found in source path".format(', '.join(files_not_exist))
        if not os.path.exists(source_path):
            error_msg = 'source path {path} not exist'.format(path=source_path)
        if error_msg:
            return {'error': error_msg}
        if not os.path.exists(dist_path):
            os.makedirs(dist_path)
        return func(*args, **kwargs)
    return wrapper
