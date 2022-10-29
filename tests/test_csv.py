from unittest import TestCase

from opylib.csv import read_file
from tests.config_tests import TestsConfig


class Test(TestCase):
    def test_read_file_w_header(self):
        fn = TestsConfig.get_instance().data_dir + \
             'test_csv_valid_w_header.csv'
        data, header = read_file(fn, True)
        self.assertEqual(header, ['col1', 'col2'])
        self.assertEqual(data, [
            ['data1', 'data2'],
            ['data3', 'data4']
        ])

    def test_read_file_wo_header(self):
        fn = TestsConfig.get_instance().data_dir + \
             'test_csv_valid_w_header.csv'
        data, _ = read_file(fn)
        self.assertEqual(data, [
            ['col1', 'col2'],
            ['data1', 'data2'],
            ['data3', 'data4']
        ])

    def test_read_file_empty(self):
        fn = TestsConfig.get_instance().data_dir + \
             'test_csv_empty.csv'
        data, _ = read_file(fn)
        self.assertEqual(data, [])

    def test_read_file_empty_expect_header(self):
        fn = TestsConfig.get_instance().data_dir + \
             'test_csv_empty.csv'
        with self.assertRaises(StopIteration):
            _ = read_file(fn, True)
