from unittest import mock, TestCase

import pika
import pytest

from tasks_client import client, sender


class TestSender(TestCase):

    def setUp(self):
        self.mocked_pika = mock.Mock()
        self.mocked_client = mock.Mock()

    def test_send_task(self):
        with mock.patch.object(client, 'Client', return_value=self.mocked_client):
            self.mocked_client.call.return_value = 'response'
            data = {
                'engines': ['enginea', 'engineb'],
                'remove': True,
                'files': ['test.json'],
            }
            response = sender.send_task(**data)
            self.assertEqual(response, self.mocked_client.call.return_value)
