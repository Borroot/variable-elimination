from network import Network, InternalNetwork
from algorithm import ve
from factor import Factor
from variable import Variable
import util

import random
import sys

sys.path.append("oracle")

from probVE import VE
from probGraphicalModels import (Alarm, Fire, Leaving, Report, Smoke, Tampering,
     Graphical_model, bn_fire_alarm, Inference_method)


if __name__ == '__main__':

    with open('output.txt', 'w') as file:
    # with sys.stdout as file:

        util.verbosity = 1  # 0, 1 or 2
        util.file = file

        # query my implementation
        network = Network('data/alarm.bif')
        query = ['Leaving', 'Smoke']
        evidence = {'Alarm': 'False'}
        factor = ve(network, query, evidence)

        # network = Network('data/survey.bif')
        # query = ['T', 'E']
        # evidence = {'R': 'small', 'A': 'adult'}
        # factor = ve(network, query, evidence)

        # query the oracle
        # Inference_method.max_display_level = 4
        # network_oracle = VE(bn_fire_alarm)
        # factor_oracle = network_oracle.query(Leaving, {Alarm: 'False'})
