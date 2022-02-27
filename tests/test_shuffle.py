from unittest import TestCase

from opylib.shuffle import shuffle


class Test(TestCase):
    def test_shuffle(self):
        a = [1, 2, 3, 4, 5, 6]  # Note that 6 goes missing as it is extra
        b = ['a', 'b', 'c', 'd', 'e']
        c = ['A', 'B', 'C', 'D', 'E']
        a, b, c = shuffle(a, b, c)

        # Ensure all lists are same length after operation
        self.assertEqual(len(a), len(b))
        self.assertEqual(len(a), len(c))

        # Make sure values in each array as still aligned
        for i, number in enumerate(a):
            lower = b[i]
            upper = c[i]
            self.assertEqual(number, ord(lower) - 96)
            self.assertEqual(number, ord(upper) - 64)

        # print(a)
        # print(b)
        # print(c)
