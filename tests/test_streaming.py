import random
from typing import List
from unittest import TestCase

from opylib.streaming import mean


class Test(TestCase):
    def test_mean(self):
        data = [10, 15, 30, 20]
        self.helper_mean(data)
        data = [random.random() * 100 for _ in range(100)]
        self.helper_mean(data)

    def helper_mean(self, data: List[float]):
        avg = 0  # Initialization does not matter
        n = 0
        for x in data:
            avg = mean(avg, n, x)
            n += 1
        self.assertAlmostEqual(avg, sum(data) / len(data),
                               msg=f'Data from failed test: {data}')
