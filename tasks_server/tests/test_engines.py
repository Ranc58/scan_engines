import uuid
import os
from unittest import mock, TestCase

import pytest

from tasks_server import engines


class TestBaseEngine(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir, capsys):
        self.tmpdir = tmpdir

    def test_init(self):
        data = {
            'remove_after_check': True,
            'files_for_check': ['test.txt'],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        engine = engines.BaseEngine(**data)
        self.assertTrue(engine)

    @mock.patch.object(uuid, 'uuid4', return_value='1234')
    def test_scan(self, mock_uuid):
        data = {
            'remove_after_check': False,
            'files_for_check': ['test.txt'],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        engine = engines.BaseEngine(**data)
        with mock.patch.object(engines.BaseEngine, '_copy_files', return_value=[]):
            result = engine.scan()
            self.assertEqual(result, {'result': 'test.txt-1234'})

    def test_copy_files(self):
        file_name = 'test.txt'
        source_path = self.tmpdir
        dist_path = self.tmpdir.mkdir("dist")
        source_path.join(file_name).write('result')
        data = {
            'remove_after_check': False,
            'files_for_check': [file_name],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        engine = engines.BaseEngine(**data)
        engine.dist_path = dist_path
        engine.source_path = source_path
        engine.files_for_check = [file_name]
        engine._copy_files()
        self.assertTrue(os.path.exists(os.path.join(dist_path, file_name)))

    def test_clear_after_check(self):
        file_name = 'test_clear.txt'
        dist_path = self.tmpdir.mkdir("dist")
        dist_path.join(file_name).write('result')
        data = {
            'remove_after_check': False,
            'files_for_check': [file_name],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        engine = engines.BaseEngine(**data)
        engine.dist_path = dist_path
        engine.files_for_check = [file_name]
        engine._clear_after_check()
        self.assertFalse(os.path.exists(os.path.join(dist_path, file_name)))

