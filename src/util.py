verbosity = 1


def print_header(text):
    if verbosity > 0:
        print('-----------------------------------------------------')
        print(text)
        print('-----------------------------------------------------\n')


def print_factors_brief(factors):
    if verbosity > 0:
        for factor in factors:
            print(factor.brief())
        print()
    if verbosity > 1:
        print_factors(factors)


def print_factor_brief(factor):
    if verbosity > 0:
        print(factor.brief())
        print()
    if verbosity > 1:
        print_factor(factor)


def print_factors(factors):
    if verbosity > 1:
        for factor in factors:
            print(factor)


def print_factor(factor):
    if verbosity > 0:
        print(factor)


def print_simple(text):
    if verbosity > 0:
        print(text)


def print_groups(query, evidence, barren):
    if verbosity > 0:
        print('Query:', ', '.join(query))
        print('Evidence:', show_evidence(evidence))
        print('Barren:', ', '.join(map(str, barren)), '\n')


def show_evidence(evidence):
    return ', '.join(map(lambda e: f'{e[0]} = {e[1]}', evidence.items()))
