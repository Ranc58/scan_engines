import uuid

from .base_engine import BaseEngine

class EngineD(BaseEngine):

    @staticmethod
    def scan(files):
        result_str = str()
        for file in files:
            result_str += '{result} from {file}\n'.format(
                file=file,
                result=str(uuid.uuid4())
            )
        return result_str
