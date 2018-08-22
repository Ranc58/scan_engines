import os
from pathlib import Path
import shutil
import uuid

from tasks_server.utils import check_dir_exist

SOURCE_PATH = os.getenv('SOURCE_PATH', os.path.join(Path().absolute(), 'source'))
DIST_PATH = os.getenv('DIST_PATH', os.path.join(Path().absolute(), 'files_storage'))


class BaseEngine:

    def __init__(self, *args, **kwargs):
        self.remove_after_check = kwargs['remove_after_check']
        self.files_for_check = kwargs['files_for_check']
        self.source_path = SOURCE_PATH
        self.dist_path = DIST_PATH

    def scan(self, result_template=None):
        copied = self._copy_files()
        if copied and copied.get('error'):
            return copied
        results_list = []
        for file in self.files_for_check:
            results_list.append(result_template.format(
                filename=file,
                result=str(uuid.uuid4())
            ))
        results = '\n'.join(results_list)
        result = {'result': f'{results}'}
        if self.remove_after_check:
            self._clear_after_check()
        return result

    @check_dir_exist
    def _copy_files(self):
        for file in self.files_for_check:
            shutil.copy(
                os.path.join(self.source_path, file),
                os.path.join(self.dist_path, file)
            )

    def _clear_after_check(self):
        for file in self.files_for_check:
            os.remove(os.path.join(self.dist_path, file))


class EngineA(BaseEngine):

    def scan(self, files=None, engine=None):
        result_template = '{filename} scanned. Result: {result}'
        return super().scan(result_template=result_template)


class EngineB(BaseEngine):

    def scan(self, files=None, engine=None):
        result_template = '{{"{filename}": "{result}"}}'
        return super().scan(result_template=result_template)


class EngineC(BaseEngine):

    def scan(self, files=None, engine=None):
        result_template = '{filename}|||{result}'
        return super().scan(result_template=result_template)


class EngineD(BaseEngine):

    def scan(self, files=None, engine=None):
        result_template = '{result} from {filename}'
        return super().scan(result_template=result_template)


class EngineE(BaseEngine):

    def scan(self, files=None, engine=None):
        result_template = 'The {filename} is {result}'
        return super().scan(result_template=result_template)
