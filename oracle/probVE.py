# probVE.py - Variable Elimination for Graphical Models
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probFactors import Factor, Factor_observed, Factor_sum, factor_times
from probGraphicalModels import (A, Alarm, B, C, Fire, Graphical_model,
                                  Grass_shiny, Grass_wet, Inference_method,
                                  Leaving, Rained, Report, Season, Shoes_wet,
                                  Smoke, Sprinkler, Tampering, bn_fire_alarm,
                                  bn_grass_watering, bn_simple1)


class VE(Inference_method):
    """The class that queries Graphical Models using variable elimination.

    gm is graphical model to query
    """

    def __init__(self, gm=None):
        self.gm = gm

    def query(self, var, obs={}, elim_order=None):
        """computes P(var|obs) where
        var is a variable
        obs is a variable:value dictionary"""
        if var in obs:
            return {val: 1 if val == obs[var] else 0 for val in var.domain}
        else:
            if elim_order == None:
                elim_order = self.gm.variables
            projFactors = [self.project_observations(fact, obs)
                           for fact in self.gm.factors]
            for v in elim_order:
                if v != var and v not in obs:
                    projFactors = self.eliminate_var(projFactors, v)
            unnorm = factor_times(var, projFactors)
            p_obs = sum(unnorm)
            self.display(1, "Unnormalized probs:", unnorm, "Prob obs:", p_obs)
            return {val: pr / p_obs for val, pr in zip(var.domain, unnorm)}

    def project_observations(self, factor, obs):
        """Returns the resulting factor after observing obs

        obs is a dictionary of variable:value pairs.
        """
        if any((var in obs) for var in factor.variables):
            # a variable in factor is observed
            return Factor_observed(factor, obs)
        else:
            return factor

    def eliminate_var(self, factors, var):
        """Eliminate a variable var from a list of factors.
        Returns a new set of factors that has var summed out.
        """
        self.display(2, "eliminating ", str(var))
        contains_var = []
        not_contains_var = []
        for fac in factors:
            if var in fac.variables:
                contains_var.append(fac)
            else:
                not_contains_var.append(fac)
        if contains_var == []:
            return factors
        else:
            newFactor = Factor_sum(var, contains_var)
            self.display(2, "Multiplying:", [f.brief() for f in contains_var])
            self.display(2, "Creating factor:", newFactor.brief())
            self.display(3, "Factor in detail", newFactor)
            not_contains_var.append(newFactor)
            return not_contains_var
