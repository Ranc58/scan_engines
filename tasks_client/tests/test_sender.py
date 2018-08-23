import sys
from unittest import mock, TestCase
from datetime import date
import os
import json

import pika
import pytest

from client import Client
import client
import sender


class TestSender(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir, capsys):
        self.tmpdir = tmpdir
        self.capsys = capsys

    def test_send_task(self):
        mocked_2_client = mock.MagicMock()
        mocked_2_client.call.return_value = 'response'
        with mock.patch('sender.Client') as mocked_client:
            mocked_client.return_value = mocked_2_client
            data = {
                'engines': ['enginea', 'engineb'],
                'remove': True,
                'files': ['test.json'],
                'host': 'localhost',
            }
            response = sender.send_task(**data)
            self.assertEqual(response, 'response')

    def test_save_results_to_file(self):
        file_path = self.tmpdir
        result = {'ENGINEA': {'result': 'ok', 'error': None}}
        sender.save_results_to_file(result, file_path)
        file_name = '{} {}.txt'.format('ENGINEA', date.today())
        file_path = os.path.join(file_path, file_name)
        expected_result = 'ok'
        with open(file_path) as f:
            result = f.read()
            self.assertEqual(result, expected_result)

    def test_output_result(self):
        dict_for_print = json.dumps({'ENGINEA': {'result': 'ok', 'error': None}})
        sender.output_result(dict_for_print)
        captured = self.capsys.readouterr()
        self.assertEqual(captured.out, "- ENGINEA:\nok\n")
