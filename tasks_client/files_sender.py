from datetime import date
import os

from client import Client


class Sender:

    def __init__(self, host, timeout, expiration):
        self.client = Client(host, timeout, expiration)
        self.results = None

    def send_tasks(self, engines, remove, files):
        data_for_call = {
            'engines': engines,
            'remove_after_check': remove,
            'files_for_check': files,
        }
        self.results = self.client.call(data_for_call)
        return self.results

    def save_results_to_file(self, file_path):
        if not self.results:
            return
        file_str = '{} {}.txt'
        current_date = date.today()
        results = self.results.get('result')
        for k, v in results.items():
            full_path = os.path.join(file_path, file_str.format(k, current_date))
            with open(full_path, 'w') as f:
                f.write(v)

    def output_result_to_cli(self):
        if not self.results:
            print('No results')
        errors = self.results.get('errors')
        results = self.results.get('result')
        if results:
            for k, v in results.items():
                print(f'- {k}:\n{v}')
        if errors:
            print('---- ERRORS ----')
            for k, v in errors.items():
                print(f'{v}')
