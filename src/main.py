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
    # query my implementation
    # util.verbosity = 2
    # network = Network('data/alarm.bif')

    # query = ['Leaving']
    # # evidence = {'Smoke': 'True', 'Leaving': 'False'}
    # evidence = {}

    # factor = ve(network, query, evidence)

    # query the oracle
    network_oracle = VE(bn_fire_alarm)
    Inference_method.max_display_level = 4
    factor_oracle = network_oracle.query(Leaving, {}, elim_order = [Report, Smoke, Alarm, Fire, Tampering])
