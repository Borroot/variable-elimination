import unittest
import sys
sys.path.extend(["src", "oracle"])

import util
from network import Network
from algorithm import ve, init_barren

# oracle imports
from probVE import VE
from probGraphicalModels import (Alarm, Fire, Leaving, Report, Smoke, Tampering,
     Graphical_model, bn_fire_alarm, Inference_method)


class TestVEAlarm(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')
        self.network_oracle = VE(bn_fire_alarm)
        util.verbosity = 0
        Inference_method.max_display_level = 0


    def test_all(self):
        # variables = [Alarm, Fire, Leaving, Report, Smoke, Tampering]
        variables = [Leaving]
        for query in variables:
            factor_oracle = self.network_oracle.query(Tampering, {})
            factor = ve(self.network, [str(query)], {})
            # print(factor_oracle)
            # print(factor)

            self.assertAlmostEqual(factor_oracle['False'], factor.values[0], 1)
            self.assertAlmostEqual(factor_oracle['True'], factor.values[1], 1)


    def tearDown(self):
        util.verbosity = 1


class TestBarrenAlarm(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')
        util.verbosity = 0


    def tearDown(self):
        util.verbosity = 1


    def test_basic(self):
        query = ['Alarm', 'Smoke']
        evidence = {'Tampering': 'True'}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Leaving', 'Report']))


    def test_0(self):
        query = ['Report', 'Smoke']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted([]))


    def test_1(self):
        query = ['Report']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Smoke']))


    def test_2(self):
        query = ['Alarm']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Leaving', 'Report', 'Smoke']))


    def test_5_0(self):
        query = ['Tampering']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Fire', 'Smoke', 'Alarm', 'Leaving', 'Report']))


    def test_5_1(self):
        query = ['Fire']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Tampering', 'Smoke', 'Alarm', 'Leaving', 'Report']))


    def test_4(self):
        query = ['Smoke']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Tampering', 'Alarm', 'Leaving', 'Report']))


class TestBarrenEarthquake(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/earthquake.bif')
        util.verbosity = 0


    def tearDown(self):
        util.verbosity = 1


    def test_1(self):
        query = ['JohnCalls']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['MaryCalls']))


    def test_2(self):
        query = ['Alarm']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['JohnCalls', 'MaryCalls']))


    def test_4(self):
        query = ['Burglary']
        evidence = {}

        barren = init_barren(self.network.variables, query, evidence)
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Earthquake', 'Alarm', 'JohnCalls', 'MaryCalls']))


if __name__ == '__main__':
    unittest.main()
