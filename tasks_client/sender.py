import argparse
import json
import os
from datetime import date

from client import Client


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser(description='Scan files.')
    parser.add_argument('-s', '--save', nargs='?', required=False,
                        type=str, help='Path to file for save results')
    parser.add_argument('-e', '--engines', nargs='*', required=True,
                        help='Select engines for scan')
    parser.add_argument('-f', '--files', nargs='*', required=True,
                        help='Select files for scan')
    parser.add_argument('-c', '--clear', action='store_true',
                        help='Delete files after check from service path')
    return parser.parse_args()


def send_task(*args, **kwargs):
    task_client = Client()
    data_for_call = {
        'engines': kwargs['engines'],
        'remove_after_check': kwargs['remove'],
        'files_for_check': kwargs['files']
    }
    response = task_client.call(data_for_call)
    return response


def save_results_to_file(response, file_path):
    file_str = '{} {}.txt'
    current_date = date.today()
    for k, v in response.items():
        if v.get('error'):
            continue
        full_path = os.path.join(file_path, file_str.format(k, current_date))
        with open(full_path, 'w') as f:
            f.write(v['result'])


def output_result(results):
    for k, v in json.loads(results).items():
        result = v.get('result')
        if v.get('error'):
            result = v.get('error')
        print(f'- {k}:\n{result}')


if __name__ == "__main__":
    user_argument = create_parser_for_user_arguments()
    engines = [engine.upper() for engine in user_argument.engines]
    files = user_argument.files
    remove_after_check = user_argument.clear
    response = send_task(
        engines=engines,
        files=files,
        remove=remove_after_check
    )
    output_result(response)
    if user_argument.save:
        save_results_to_file(json.loads(response), user_argument.save)
