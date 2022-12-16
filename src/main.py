from network import Network, InternalNetwork
from algorithm import ve


if __name__ == '__main__':
    network = Network('data/survey.bif')

    print(network.variables)

    for factor in network.factors:
        print(factor)
        print()

    factor = network.variable_to_factor(network.name_to_variable('E'))
    print('---------------------------------')
    print(factor)
    print()
    print(factor.reduce(network.name_to_variable('A'), 'adult'))

    # query = ['Alarm', 'Smoke']
    # evidence = {'Tampering': 'True'}

    # ve(network, query, evidence, [])

    # Determine your elimination ordering before you call the run function. The elimination ordering
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points.
