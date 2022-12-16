import unittest
import sys
sys.path.append("src")

from network import Network
from factor import Factor


class TestFactor(unittest.TestCase):


    def setUp(self):
        self.network = Network('data/alarm.bif')


    def test_basic(self):
        query = ['Alarm', 'Smoke']
        evidence = {'Tampering': 'True'}

        barren = barren_nodes(self.network.variables, query, list(evidence.keys()))
        barren = sorted(list(map(lambda node: node.name, barren)))

        self.assertEqual(barren, sorted(['Leaving', 'Report']))


if __name__ == '__main__':
    unittest.main()
