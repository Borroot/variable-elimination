import unittest
import sys
sys.path.append("src")

from network import Network
from factor import Factor


class TestMarginalizeT(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/survey.bif')


    def test_1(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        margin = factor.marginalize(self.network.name_to_variable('O'))

        self.assertEqual(margin.values,
            [0.58+0.70, 0.18+0.09, 0.24+0.21, 0.48+0.56, 0.10+0.08, 0.42+0.36])


    def test_2(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        margin = factor.marginalize(self.network.name_to_variable('R'))

        self.assertEqual(margin.values,
            [0.58+0.48, 0.18+0.10, 0.24+0.42, 0.70+0.56, 0.09+0.08, 0.21+0.36])


    def test_3(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        margin = factor.marginalize(self.network.name_to_variable('T'))

        for value in margin.values:
            self.assertAlmostEqual(value, 1, 2)


class TestMarginalizeE(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/survey.bif')


    def test_1(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        margin = factor.marginalize(self.network.name_to_variable('A'))

        self.assertEqual(margin.values,
            [0.70+0.90+0.64, 0.72+0.88+0.75, 0.30+0.10+0.36, 0.28+0.12+0.25])


    def test_2(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        margin = factor.marginalize(self.network.name_to_variable('E'))

        self.assertEqual(margin.values, [1, 1, 1, 1, 1, 1])


    def test_3(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        margin = factor.marginalize(self.network.name_to_variable('S'))

        self.assertEqual(margin.values,
            [0.70+0.72, 0.30+0.28, 0.90+0.88, 0.10+0.12, 0.64+0.75, 0.36+0.25])


class TestReduceT(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/survey.bif')


    def test_1(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('R'), 'small')

        self.assertEqual(reduce.values, [0.48, 0.10, 0.42, 0.56, 0.08, 0.36])


    def test_2(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('R'), 'big')

        self.assertEqual(reduce.values, [0.58, 0.18, 0.24, 0.70, 0.09, 0.21])


    def test_3(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('O'), 'emp')

        self.assertEqual(reduce.values, [0.58, 0.18, 0.24, 0.48, 0.10, 0.42])


    def test_4(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('O'), 'self')

        self.assertEqual(reduce.values, [0.70, 0.09, 0.21, 0.56, 0.08, 0.36])


    def test_5(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('T'), 'car')

        self.assertEqual(reduce.values, [0.58, 0.48, 0.70, 0.56])


    def test_6(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('T'), 'other')

        self.assertEqual(reduce.values, [0.18, 0.10, 0.09, 0.08])


    def test_7(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('T'))
        reduce = factor.reduce(self.network.name_to_variable('T'), 'train')

        self.assertEqual(reduce.values, [0.24, 0.42, 0.21, 0.36])


class TestReduceE(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/survey.bif')


    def test_1(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('A'), 'adult')

        self.assertEqual(reduce.values, [0.70, 0.72, 0.30, 0.28])


    def test_2(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('A'), 'old')

        self.assertEqual(reduce.values, [0.90, 0.88, 0.10, 0.12])


    def test_3(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('A'), 'young')

        self.assertEqual(reduce.values, [0.64, 0.75, 0.36, 0.25])


    def test_4(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('E'), 'high')

        self.assertEqual(reduce.values, [0.70, 0.72, 0.90, 0.88, 0.64, 0.75])


    def test_5(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('E'), 'uni')

        self.assertEqual(reduce.values, [0.30, 0.28, 0.10, 0.12, 0.36, 0.25])


    def test_6(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('S'), 'F')

        self.assertEqual(reduce.values, [0.70, 0.30, 0.90, 0.10, 0.64, 0.36])


    def test_7(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('E'))
        reduce = factor.reduce(self.network.name_to_variable('S'), 'M')

        self.assertEqual(reduce.values, [0.72, 0.28, 0.88, 0.12, 0.75, 0.25])


if __name__ == '__main__':
    unittest.main()
