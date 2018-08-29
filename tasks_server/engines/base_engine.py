
class BaseEngine:

    @staticmethod
    def scan(files):
        raise NotImplementedError('Method should be overridden in the child class')
