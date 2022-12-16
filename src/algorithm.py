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


def barren_nodes(variables, query, evidence):
    """
    Compute the barren nodes: neither queried, nor observed and no children or
    only barren nodes as children.
    """

    # the query and evidence variables are for sure not barren
    nonbarren = query + evidence  # list with type variable.name
    barren = []                   # list with type variable

    # recurs down from all of the topnodes, i.e. nodes without parents
    topnodes = [variable for variable in variables if len(variable.parents) == 0]
    for variable in topnodes:
        if barren_recurs(variable, nonbarren, barren) and not variable in barren:
            barren.append(variable)

    return sorted(barren)


def ve(network, query, evidence, order):
    """
    Use the variable elimination algorithm to find out the probability
    distribution of the query variables given the observed variables.
    """
    assert all(e in map(lambda v: v.name, network.variables) for e in evidence.keys())
    assert all(q in map(lambda v: v.name, network.variables) for q in query)

    # TODO order as list or ordering algorithm

    # compute the barren nodes
    barren = barren_nodes(network.variables, query, list(evidence.keys()))

    print('Query:', *query, '| Evidence:', *evidence)
    print('Barren:', *barren)
