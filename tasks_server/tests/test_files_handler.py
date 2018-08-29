import os

from unittest import mock, TestCase
import pytest

from tasks_server import files_handler


def func_for_dec(*args, **kwargs):
    return 2+2


class TestFileHandler(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir, capsys):
        self.tmpdir = tmpdir

    def test_init(self):
        handler = files_handler.FileHandler({'engines': ['ENGINEA']})
        self.assertTrue(handler)

    def test_filter_dirs(self):
        data = {
            'engines': ['ENGINEA'],
            'remove_after_check': True,
            'files_for_check': ['test.txt'],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        handler = files_handler.FileHandler(data)
        handler._filter_dirs()
        expected_error_msg = 'file test.txt not found in {}.'.format(self.tmpdir)
        self.assertEqual(handler.response['errors'], {'test.txt': expected_error_msg})

    def test_filter_engines(self):
        data = {
            'engines': ['ENGINEA', 'ENGINEFf'],
            'remove_after_check': True,
            'files_for_check': ['test.txt'],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,
        }
        handler = files_handler.FileHandler(data)
        handler._filter_engines()
        expected_error_msg = 'engine ENGINEFf not found.'
        self.assertEqual(handler.response['errors'], {'ENGINEFf': expected_error_msg})

    def test_check_dir_exist(self):
        mock_class = mock.Mock()
        mock_class.dist_path = str(self.tmpdir)
        mock_class.source_path = str(self.tmpdir)
        mock_class.engines = ['ENGINEA']
        mock_class.files_for_check = ['file.txt']
        mock_class._filter_dirs.return_value = []
        mock_class._filter_engines.return_value = []
        result = files_handler.FileHandler.check_dir_exist(func_for_dec)
        self.assertEqual(result(mock_class), 4)

    def test_get_info(self):
        mocked_engine = mock.Mock()
        mocked_engine.scan.return_value = {'result': 'result'}
        self.tmpdir.join('test.txt').write('result')
        with mock.patch.dict(files_handler.FileHandler.ENGINES, {'ENGINEA': mocked_engine}):
            data = {
                'engines': ['ENGINEA', 'ENGINEFf'],
                'remove_after_check': False,
                'files_for_check': ['test.txt'],
                'dist_path': os.path.join(self.tmpdir, 'sub'),
                'source_path': self.tmpdir,
            }
            handler = files_handler.FileHandler(data)
            result = handler.get_info()
            self.assertEqual(result['errors'], {'ENGINEFf': 'engine ENGINEFf not found.'})
            self.assertEqual(result['result'], {'ENGINEA': mocked_engine.scan.return_value})

    def test_clear_after_check(self):
        file_name = 'test_clear.txt'
        dist_path = self.tmpdir.mkdir("dist")
        dist_path.join(file_name).write('result')
        data = {
            'engines': ['ENGINEA', 'ENGINEFf'],
            'remove_after_check': True,
            'files_for_check': [file_name],
            'dist_path': os.path.join(self.tmpdir, 'sub'),
            'source_path': self.tmpdir,

        }
        handler = files_handler.FileHandler(data)
        handler.dist_path = dist_path
        handler.files_for_check = [file_name]
        handler._filtred_files_for_check = [file_name]
        handler._clear_after_check()
        self.assertFalse(os.path.exists(os.path.join(dist_path, file_name)))
