from unittest import TestCase

from opylib.list_tools import max_w_ind, min_w_ind


class Test(TestCase):
    def test_max_w_ind(self):
        lst = list(range(10))
        ind, val = max_w_ind(lst)
        self.assertEqual(ind, 9)
        self.assertEqual(val, 9)

        lst = [5, 3, 8, 2, 6]
        ind, val = max_w_ind(lst)
        self.assertEqual(ind, 2)
        self.assertEqual(val, 8)

    def test_min_w_ind(self):
        lst = list(range(10))
        ind, val = min_w_ind(lst)
        self.assertEqual(ind, 0)
        self.assertEqual(val, 0)

        lst = [5, 3, 8, 2, 6]
        ind, val = min_w_ind(lst)
        self.assertEqual(ind, 3)
        self.assertEqual(val, 2)
