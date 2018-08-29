import os
import shutil

from engines import EngineA, EngineB, EngineC, EngineD, EngineE


class FileHandler:

    ENGINES = {
        'ENGINEA': EngineA,
        'ENGINEB': EngineB,
        'ENGINEC': EngineC,
        'ENGINED': EngineD,
        'ENGINEE': EngineE,
    }

    def __init__(self, files_data):
        self.engines_path = os.path.join(os.getcwd(), 'engines')
        self.engines = files_data.get('engines')
        self.source_path = files_data.get('source_path')
        self.dist_path = files_data.get('dist_path')
        self.files_for_check = files_data.get('files_for_check')
        self.remove_after_check = files_data.get('remove_after_check')
        self._filtred_engines = None
        self._filtred_files_for_check = None
        self.response = {'errors': {}, 'result': {}}

    def _filter_dirs(self):
        files_not_exist = []
        for file in self.files_for_check:
            if not os.path.isfile(os.path.join(self.source_path, file)):
                files_not_exist.append(file)
                self.response['errors'].update(
                    {file: 'file {file} not found in {path}.'.format(
                        file=file,
                        path=self.source_path)
                    }
                )
        return files_not_exist

    def _filter_engines(self):
        engines_not_exist = set(self.engines) - set(list(self.ENGINES.keys()))
        for engine in engines_not_exist:
            self.response['errors'].update(
               {engine: 'engine {engine} not found.'.format(engine=engine)})
        return engines_not_exist

    def check_dir_exist(func):
        def wrapper(*args, **kwargs):
            obj = args[0]
            if not os.path.exists(obj.source_path):
                error_msg = 'Source path {path} not exist.'.format(
                    path=obj.source_path
                )
                obj.response['errors'].update({
                    'source_error': error_msg
                })
                return obj.response
            obj._filtred_files_for_check = list(
                set(obj.files_for_check) - set(obj._filter_dirs())
            )
            obj._filtred_engines = list(
                set(obj.engines) - set(obj._filter_engines())
            )
            if not os.path.exists(obj.dist_path):
                os.makedirs(obj.dist_path)
            return func(obj)
        return wrapper

    def _copy_files(self):
        for file in self._filtred_files_for_check:
            shutil.copy(
                os.path.join(self.source_path, file),
                os.path.join(self.dist_path, file)
            )

    @check_dir_exist
    def get_info(self):
        self._copy_files()
        for engine in self._filtred_engines:
            engine_object = self.ENGINES.get(engine)
            result = engine_object.scan(self._filtred_files_for_check)
            if not result:
                continue
            self.response['result'].update({
                engine: result
            })
        if self.remove_after_check:
            self._clear_after_check()
        return self.response

    def _clear_after_check(self):
        for file in self._filtred_files_for_check:
            os.remove(os.path.join(self.dist_path, file))
