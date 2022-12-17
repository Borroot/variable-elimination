import unittest
import sys
sys.path.append("src")

from network import Network
from factor import Factor
from variable import Variable


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


class TestReduceSmall(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')


    def test_1(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('Tampering'))
        reduce = factor.reduce(self.network.name_to_variable('Tampering'), 'False')

        self.assertEqual(reduce.values, [0.98])


    def test_2(self):
        factor = self.network.variable_to_factor(self.network.name_to_variable('Tampering'))
        reduce = factor.reduce(self.network.name_to_variable('Tampering'), 'True')

        self.assertEqual(reduce.values, [0.02])


class TestReduceSmallProduct(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')


    def test_1(self):
        factor1 = self.network.variable_to_factor(self.network.name_to_variable('Tampering'))
        reduce1 = factor1.reduce(self.network.name_to_variable('Tampering'), 'False')

        factor2 = self.network.variable_to_factor(self.network.name_to_variable('Alarm'))
        reduce2 = factor2.reduce(self.network.name_to_variable('Tampering'), 'False')

        product = reduce1.product(reduce2)
        answer = [0.98*0.9999, 0.98*0.01, 0.98*0.0001, 0.98*0.99]
        for value1, value2 in zip(product.values, answer):
            self.assertAlmostEqual(value1, value2)


class TestReduceSmall(unittest.TestCase):


    def test_1(self):
        va = Variable("A", map(str, range(3)))
        vb = Variable("B", map(str, range(2)))
        vc = Variable("C", map(str, range(2)))

        factor1 = Factor([va, vb], [0.5, 0.8, 0.1, 0, 0.3, 0.9])
        factor2 = Factor([vb, vc], [0.5, 0.7, 0.1, 0.2])

        product_factor = factor1.product(factor2)
        answer = [0.25, 0.35, 0.08, 0.16, 0.05, 0.07, 0, 0, 0.15, 0.21, 0.09, 0.18]
        for value1, value2 in zip(product_factor.values, answer):
            self.assertAlmostEqual(value1, value2)


    def test_2(self):
        va = Variable("A", map(str, range(1)))

        factor1 = Factor([va], [0.5])
        factor2 = Factor([va], [0.2])

        product_factor = factor1.product(factor2)
        answer = [0.1]
        for value1, value2 in zip(product_factor.values, answer):
            self.assertAlmostEqual(value1, value2)


    def test_3(self):
        va = Variable("A", map(str, range(2)))

        factor1 = Factor([va], [0.5, 0.1])
        factor2 = Factor([va], [0.2, 0.1])

        product_factor = factor1.product(factor2)
        answer = [0.1, 0.01]
        for value1, value2 in zip(product_factor.values, answer):
            self.assertAlmostEqual(value1, value2)


    def test_4(self):
        va = Variable("A", map(str, range(3)))

        factor1 = Factor([va], [0.5, 0.1, 0.02])
        factor2 = Factor([va], [0.2, 0.1, 0.001])

        product_factor = factor1.product(factor2)
        answer = [0.1, 0.01, 0.0002]
        for value1, value2 in zip(product_factor.values, answer):
            self.assertAlmostEqual(value1, value2, 2)


    def test_5(self):
        va = Variable("A", map(str, range(2)))
        vb = Variable("B", map(str, range(3)))

        factor1 = Factor([va], [0.5, 0.1])
        factor2 = Factor([va, vb], [200, 400, 250, 10, 50, 20])

        product_factor = factor1.product(factor2)
        self.assertEqual(product_factor.values, [100, 200, 125, 1, 5, 2])


    def test_6(self):
        va = Variable("A", map(str, range(2)))
        vb = Variable("B", map(str, range(3)))
        vc = Variable("C", map(str, range(3)))

        factor1 = Factor([va, vb, vc],
            [15, 33, 55, 36, 56, 89, 76, 38, 19, 37, 32, 39, 10, 29, 23, 99, 72, 58])
        factor2 = Factor([va, vc], [28, 84, 66, 61, 86, 34])

        product_factor = factor1.product(factor2)
        self.assertEqual(product_factor.values,
            [420, 2772, 3630, 1008, 4704, 5874, 2128, 3192, 1254, 2257,
             2752, 1326, 610, 2494, 782, 6039, 6192, 1972])


    def test_7(self):
        va = Variable("A", map(str, range(2)))
        vb = Variable("B", map(str, range(3)))
        vc = Variable("C", map(str, range(3)))

        factor1 = Factor([va, vb, vc],
            [15, 33, 55, 36, 56, 89, 76, 38, 19, 37, 32, 39, 10, 29, 23, 99, 72, 58])
        factor2 = Factor([va, vc], [28, 84, 66, 61, 86, 34])

        product_factor = factor2.product(factor1)
        self.assertEqual(product_factor.values,
            [420, 2772, 3630, 1008, 4704, 5874, 2128, 3192, 1254, 2257,
             2752, 1326, 610, 2494, 782, 6039, 6192, 1972])


if __name__ == '__main__':
    unittest.main()
