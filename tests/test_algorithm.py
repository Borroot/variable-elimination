import unittest
import sys
sys.path.append("src")

from network import Network
from algorithm import ve, barren_nodes


class TestBarrenAlarm(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')


    def test_basic(self):
        query = ['Alarm', 'Smoke']
        evidence = {'Tampering': 'True'}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Leaving', 'Report']))


    def test_0(self):
        query = ['Report', 'Smoke']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted([]))


    def test_1(self):
        query = ['Report']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Smoke']))


    def test_2(self):
        query = ['Alarm']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Leaving', 'Report', 'Smoke']))


    def test_5_0(self):
        query = ['Tampering']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Fire', 'Smoke', 'Alarm', 'Leaving', 'Report']))


    def test_5_1(self):
        query = ['Fire']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Tampering', 'Smoke', 'Alarm', 'Leaving', 'Report']))


    def test_4(self):
        query = ['Smoke']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Tampering', 'Alarm', 'Leaving', 'Report']))


class TestBarrenEarthquake(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/earthquake.bif')


    def test_1(self):
        query = ['JohnCalls']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['MaryCalls']))


    def test_2(self):
        query = ['Alarm']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['JohnCalls', 'MaryCalls']))


    def test_4(self):
        query = ['Burglary']
        evidence = {}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Earthquake', 'Alarm', 'JohnCalls', 'MaryCalls']))


if __name__ == '__main__':
    unittest.main()
