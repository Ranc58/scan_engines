import argparse

from files_sender import Sender


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
    parser.add_argument('-r', '--rabbit', nargs='?', required=False, default='localhost',
                        type=str, help='host for RabbitMQ')
    parser.add_argument('-t', '--timeout', nargs='?', required=False, default=30,
                        type=int, help='timeout for awaiting answer from server')
    parser.add_argument('-x', '--expiration', nargs='?', required=False, default=60,
                        type=int, help='expiration time for message')
    return parser.parse_args()


if __name__ == "__main__":
    user_argument = create_parser_for_user_arguments()
    engines = [engine.upper() for engine in user_argument.engines]
    files = user_argument.files
    remove_after_check = user_argument.clear
    rabbit_host = user_argument.rabbit
    timeout = user_argument.timeout
    expiration = user_argument.expiration
    sender = Sender(rabbit_host, timeout, expiration)
    sender.send_tasks(engines, remove_after_check, files)
    sender.output_result_to_cli()
    if user_argument.save:
        sender.save_results_to_file(user_argument.save)
