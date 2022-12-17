import util

import random


def barren_recurs(variable, nonbarren, barren):
    """
    Compute the barren nodes recursively. This function returns whether a given
    variable is a barren node. All the barren nodes are added to the provided
    list. The nonbarren list consists of the query and evidence variable names.
    """

    # if the variable is either a query or evidence variable it is not barren
    if variable.name in nonbarren:
        for child in variable.children:
            barren_recurs(child, nonbarren, barren)
        return False

    # if the variable has no children it is barren
    if len(variable.children) == 0:
        if not variable in barren: barren.append(variable)
        return True

    # if all children are barren then we are also barren
    if all(barren_recurs(child, nonbarren, barren) for child in variable.children):
        if not variable in barren: barren.append(variable)
        return True

    # recurs down the tree to check the other nodes
    for child in variable.children:
        barren_recurs(child, nonbarren, barren)
    return False


def init_barren(variables, query, evidence):
    """
    Compute the barren nodes: neither queried, nor observed and no children or
    only barren nodes as children.
    """

    # the query and evidence variables are for sure not barren
    nonbarren = query + list(evidence.keys())  # list with type variable.name
    barren = []  # list with type variable

    # recurs down from all of the topnodes, i.e. nodes without parents
    topnodes = [variable for variable in variables if len(variable.parents) == 0]
    for variable in topnodes:
        if barren_recurs(variable, nonbarren, barren) and not variable in barren:
            barren.append(variable)
    barren.sort()

    util.print_header('Running VE on the following setup')
    util.print_groups(query, evidence, barren)

    return barren


def init_factors(network, evidence, barren):
    """Construct the nonbarren reduced factors from the network."""

    # create a list with all the factors for nonbarren variables
    factors = [network.variable_to_factor(variable)
        for variable in network.variables if variable not in barren]

    # util.print_header('Factors of nonbarren nodes')
    # util.print_factors(factors)

    # reduce all of the factors for the evidence given
    for evidence_name, value in evidence.items():
        for i in range(len(factors)):
            evidence_variable = network.name_to_variable(evidence_name)
            if evidence_variable in factors[i].variables:
                factors[i] = factors[i].reduce(evidence_variable, value)

    util.print_header(
        'Reduced factors of nonbarren nodes based on evidence\n'
        'Evidence: {}'.format(util.show_evidence(evidence)))
    util.print_factors_brief(factors)

    return factors


def init_order(network, query, evidence, barren, order):
    """Construct the order, either abritrary, from the given order, or using the given algorithm."""

    util.print_header('Elimination order')

    # compute all the variables that should be marginalized
    marginalize = [variable for variable in network.variables if variable not in barren and
        variable.name not in evidence.keys() and variable.name not in query]

    # use an arbitrary order if no instructions are given
    if order is None:
        print('No elimination order instructions are given')
        print('An arbitrary elimination order is chosen')
        print(f'\nOrder: {marginalize}\n')
        return marginalize

    # use the order that is given
    if type(order) is list:
        # check if the given order uses the correct variables
        assert len(set(list(map(lambda variable: variable.name, marginalize)) + order)) == len(order)

        order = list(map(network.name_to_variable, order))
        print('An elimination order was provided')
        print(f'\nOrder: {order}\n')
        return order

    # TODO elimination order algorithm is given


def multiply_final(factors):
    """Multiply all the given factors together."""

    # sort the factors based on size
    factors.sort(key = lambda factor: len(factor.variables))

    print('Multiplying the following factors:\n')
    util.print_factors_brief(factors)

    # multiply the factors
    final_factor = factors[0]
    for factor in factors[1:]:
        final_factor = final_factor.product(factor)

    print(f'Resulting in:\n\n{final_factor.brief()}\n')
    return final_factor


def multiply(factors, variable):
    """Multiply all the factors containing the given variable."""

    # take out all the factors which we need to multiply
    product_factors = []
    new_factors = []
    for factor in factors:
        if variable in factor.variables:
            product_factors.append(factor)
        else:
            new_factors.append(factor)

    # sort the factors based on size
    product_factors.sort(key = lambda factor: len(factor.variables))

    print('Multiplying the following factors:\n')
    util.print_factors_brief(product_factors)

    # multiply the factors
    final_factor = product_factors[0]
    for factor in product_factors[1:]:
        final_factor = final_factor.product(factor)

    print(f'Resulting in:\n\n{final_factor.brief()}\n')
    return new_factors, final_factor


def marginalize(factor, variable):
    marginalized_factor = factor.marginalize(variable)

    print(f'Marginalizing over {variable} gives:\n')
    print(marginalized_factor.brief(), '\n')

    return marginalized_factor


def ve(network, query, evidence, order = None):
    """
    Use the variable elimination algorithm to find out the probability
    distribution of the query variables given the observed variables.
    """
    assert all(e in map(lambda v: v.name, network.variables) for e in evidence.keys())
    assert all(q in map(lambda v: v.name, network.variables) for q in query)

    # compute the barren variables
    barren = init_barren(network.variables, query, evidence)

    # determine the elimination order
    order = init_order(network, query, evidence, barren, order)

    # compute the nonbarren reduced factors
    factors = init_factors(network, evidence, barren)

    util.print_header(
        f'Main loop of VE, going over all the variables\n'
        f'Order: {order}')
    util.print_factors_brief(factors)

    for variable in order:
        util.print_header(f'Processing variable {variable}')

        # multiply all factors containing the variable under consideration
        factors, multiplied_factor = multiply(factors, variable)

        # marginalize the variable
        factors.append(marginalize(multiplied_factor, variable))

        print('The new factors are:\n')
        util.print_factors_brief(factors)

    util.print_header(f'Multiple the final factors')
    factor = multiply_final(factors)

    util.print_header(f'Normalization and final factor')
    factor = factor.normalize()

    # the final result of VE
    print(factor)
