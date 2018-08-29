from unittest import mock, TestCase
from datetime import date
import os

import pytest

import files_sender


class TestFilesSender(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir, capsys):
        self.tmpdir = tmpdir
        self.capsys = capsys

    def test_init(self):
        with mock.patch('files_sender.Client'):
            sender = files_sender.Sender('localhost', 20, 60)
            self.assertTrue(sender)

    def test_send_tasks(self):
        mocked_2_client = mock.Mock()
        mocked_2_client.call.return_value = 'response'
        with mock.patch('files_sender.Client', return_value=mocked_2_client):
            sender = files_sender.Sender('localhost', 20, 60)
            # mocked_client.return_value = mocked_2_client
            data = {
                'engines': ['enginea', 'engineb'],
                'remove': True,
                'files': ['test.json'],
            }
            response = sender.send_tasks(**data)
            self.assertEqual(response, 'response')

    def test_save_result_to_file(self):
        file_path = self.tmpdir
        dict_for_print = {'result': {'ENGINEA': 'ok'}}
        sender = files_sender.Sender('localhost', 20, 60)
        sender.results = dict_for_print
        sender.save_results_to_file( file_path)
        file_name = '{} {}.txt'.format('ENGINEA', date.today())
        file_path = os.path.join(file_path, file_name)
        expected_result = 'ok'
        with open(file_path) as f:
            result = f.read()
            self.assertEqual(result, expected_result)

    def test_output_result(self):
        dict_for_print = {'result': {'ENGINEA': 'ok'}}
        sender = files_sender.Sender('localhost', 20, 60)
        sender.results = dict_for_print
        sender.output_result_to_cli()
        captured = self.capsys.readouterr()
        self.assertEqual(captured.out, "- ENGINEA:\nok\n")
