import uuid
import os
from unittest import mock, TestCase

import pytest


import engines

class TestEngineA(TestCase):

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        files = ['file_1']
        result = engines.engine_a.EngineA.scan(files)
        self.assertEqual(result, 'file_1 scanned. Result: 1234\n')


class TestEngineB(TestCase):

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        files = ['file_1']
        result = engines.engine_b.EngineB.scan(files)
        self.assertEqual(result, '{"file_1": "1234"}\n')


class TestEngineC(TestCase):

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        files = ['file_1']
        result = engines.engine_c.EngineC.scan(files)
        self.assertEqual(result, 'file_1|||1234\n')


class TestEngineD(TestCase):

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        files = ['file_1']
        result = engines.engine_d.EngineD.scan(files)
        self.assertEqual(result, '1234 from file_1\n')


class TestEngineE(TestCase):

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        files = ['file_1']
        result = engines.engine_e.EngineE.scan(files)
        self.assertEqual(result, 'The file_1 is 1234\n')


