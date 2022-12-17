from network import Network, InternalNetwork
from algorithm import ve
from factor import Factor
from variable import Variable

import random


if __name__ == '__main__':
    network = Network('data/survey.bif')

    query = ['Alarm', 'Smoke']
    evidence = {'Tampering': 'True'}

    ve(network, query, evidence, [])

    # Determine your elimination ordering before you call the run function. The elimination ordering
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points.
