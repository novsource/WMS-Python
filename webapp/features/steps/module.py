import unittest
from webapp.analysis import analysis


class TestModuleAnalysis(unittest.TestCase):

    def test_min_max_01(self):
        data = [[1, 'Дерево ', 'Zara', 'г. Иркутск улица Пушкина', 46, 73, 5],
                [2, 'Дерево ', 'Все для дома', 'г. Иркутск улица Пушкина', 2, 16, 1]]

        data_check = [[1, 'Дерево ', 'Zara', 'г. Иркутск улица Пушкина', 55, 87, 5],
                      [2, 'Дерево ', 'Все для дома', 'г. Иркутск улица Пушкина', 2, 15, 1]]

        self.assertEqual(data_check, analysis.create_new_min_max_with_data({1: -20, 2: 5}, data))
