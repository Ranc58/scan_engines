import uuid

from .base_engine import BaseEngine


class EngineC(BaseEngine):

    @staticmethod
    def scan(files):
        result_str = str()
        for file in files:
            result_str += '{file}|||{result}\n'.format(
                file=file,
                result=str(uuid.uuid4())
            )
        return result_str
