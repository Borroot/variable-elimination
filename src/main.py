from network import Network, InternalNetwork
from algorithm import ve

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    network = Network('data/survey.bif')

    print(network.variables)

    for factor in network.factors:
        print(factor)

    factor = network.variable_to_factor(network.name_to_variable('T'))
    print('-------------')
    print(factor)
    print(factor.reduce(network.name_to_variable('R'), 'small'))

    # query = ['Alarm', 'Smoke']
    # evidence = {'Tampering': 'True'}

    # ve(network, query, evidence, [])

    # Determine your elimination ordering before you call the run function. The elimination ordering
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points.
