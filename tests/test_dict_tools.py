from unittest import TestCase

from opylib.dict_tools import merge_dict2, merge_dicts, merge_two_dicts


class Test(TestCase):
    def test_merge_dicts(self):
        d1 = self.helper_d1()
        d2 = self.helper_d2()
        d3 = self.helper_d3()
        d4 = self.helper_d4()
        self.assertEqual(merge_dicts(d1, d2, d3, d4), {**d1, **d2, **d3, **d4})

    def test_merge_two_dicts(self):
        d1 = self.helper_d1()
        d2 = self.helper_d2()
        self.assertEqual(merge_two_dicts(d1, d2), {**d1, **d2})

    def test_merge_dict2(self):
        d1 = self.helper_d1()
        d2 = self.helper_d2()
        self.assertEqual(merge_dict2(d1, d2), {**d1, **d2})

    @staticmethod
    def helper_d1():
        return {
            'a': 'Aye',
            'b': 'Bee',
            'c': 'Cee',
        }

    @staticmethod
    def helper_d2():
        return {
            'c': 'C',
            'd': 'D',
            'e': 'E',
        }

    @staticmethod
    def helper_d3():
        return {
            'd': 'Dee',
            'f': 'F'
        }

    @staticmethod
    def helper_d4():
        return {
            'a': 'aye...',
            'f': 'Free',
        }
