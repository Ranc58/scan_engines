from unittest import mock, TestCase


from tasks_server import files_handler


class TestFileHandler(TestCase):

    def test_init(self):
        handler = files_handler.FileHandler({'engine': 'ENGINEA'})
        self.assertTrue(handler)

    def test_return_error(self):
        handler = files_handler.FileHandler({'engine': 'ENGINEA'})
        error_msg = 'error'
        result = handler.return_error(error_msg)
        self.assertEqual(result, {'error': error_msg})

    def test_get_info(self):
        scan_mock = mock.Mock()
        scan_mock.scan.return_value = {'result': 'result'}
        mocked_engine = mock.Mock()
        mocked_engine.return_value = scan_mock
        with mock.patch.dict(files_handler.FileHandler.ENGINES, {'ENGINEA': mocked_engine}):
            handler = files_handler.FileHandler({'engine': 'ENGINEA'})
            result = handler.get_info()
            self.assertEqual(result, scan_mock.scan.return_value)

