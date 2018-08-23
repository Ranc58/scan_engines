
from unittest import mock, TestCase
import pytest

from tasks_server import utils


def func_for_dec(*args, **kwargs):
    return 2+2


class TestUtils(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir, capsys):
        self.tmpdir = tmpdir

    def test_does_file_exist_in_dir_not_exist(self):
        test_files = ["test_file.txt"]
        response = utils._does_file_exist_in_dir(str(self.tmpdir), test_files)
        self.assertEqual(response, test_files)

    def test_does_file_exist_in_dir(self):
        tmp_dir = self.tmpdir.mkdir("sub")
        tmp_dir.join('test_exist_file.txt').write('result')
        test_files = ["test_exist_file.txt"]
        response = utils._does_file_exist_in_dir(tmp_dir, test_files)
        self.assertEqual(response, [])

    def test_check_dir_exist(self):
        with mock.patch.object(utils, '_does_file_exist_in_dir', return_value=[]):
            mock_class = mock.Mock()
            mock_class.dist_path = str(self.tmpdir)
            mock_class.source_path = str(self.tmpdir)
            mock_class.files_for_check = ['file.txt']
            result = utils.check_dir_exist(func_for_dec)
            self.assertEqual(result(mock_class), 4)
