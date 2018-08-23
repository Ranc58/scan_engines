from unittest import mock, TestCase

import pika
from client import Client


class TestClient(TestCase):

    def setUp(self):
        self.mocked_pika = mock.Mock()

    def test_init_client(self):
        with mock.patch.object(pika, 'BlockingConnection', return_value=self.mocked_pika):
            test_client = Client()
            self.assertTrue(test_client)

    def test_on_response(self):
        with mock.patch.object(pika, 'BlockingConnection', return_value=self.mocked_pika):
            test_client = Client()
            props = mock.Mock()
            props.correlation_id = test_client.corr_id
            test_client.on_response(None, None, props, 'test_body')
            self.assertEqual(test_client.response, 'test_body')

    def test_call(self):
        with mock.patch.object(pika, 'BlockingConnection', return_value=self.mocked_pika):
            with mock.patch.object(pika, 'BasicProperties', return_value=self.mocked_pika):
                test_client = Client()
                props = mock.Mock()
                props.correlation_id = test_client.corr_id
                test_client.response = b'test'
                result = test_client.call({'test_key': 'test_val'})
                self.assertEqual(result, 'test')
