import engines


class FileHandler:

    ENGINES = {
        'ENGINEA': engines.EngineA,
        'ENGINEB': engines.EngineB,
        'ENGINEC': engines.EngineC,
        'ENGINED': engines.EngineE,
        'ENGINEE': engines.EngineD,
    }

    def __init__(self, files_data):
        self.engine_name = files_data.get('engine')
        self.engine = self.ENGINES.get(self.engine_name)
        self.files_data = files_data

    def return_error(self, error_msg):
        return {'error': error_msg}

    def get_info(self):
        if not self.engine:
            msg = 'engine {engine} not found. Available engines: {engines}'
            error_msg = msg.format(
                engine=self.engine_name,
                engines=', '.join([k for k, v in self.ENGINES.items()])
            )
            return self.return_error(error_msg)
        engine = self.engine(**self.files_data)
        result = engine.scan()
        if result.get('error'):
            error_msg = result.get('error')
            return self.return_error(error_msg)
        return {'result': result['result']}
