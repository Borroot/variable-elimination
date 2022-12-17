from network import Network, InternalNetwork
from algorithm import ve
from factor import Factor
from variable import Variable

import random


if __name__ == '__main__':
    network = Network('data/alarm.bif')

    query = ['Tampering']
    evidence = {'Smoke': 'True', 'Leaving': 'False'}

    ve(network, query, evidence, order = ['Fire', 'Alarm'])
