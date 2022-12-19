import sys


verbosity = 1
file = sys.stdout


def print_header(text):
    if verbosity > 0:
        print('-----------------------------------------------------', file = file)
        print(text, file = file)
        print('-----------------------------------------------------\n', file = file)


def print_factors_brief(factors):
    if verbosity > 0:
        for factor in factors:
            print(factor.brief(), file = file)
        print('', file = file)
    if verbosity > 1:
        print_factors(factors)


def print_factor_brief(factor):
    if verbosity > 0:
        print(factor.brief(), file = file)
        print('', file = file)
    if verbosity > 1:
        print_factor(factor)


def print_factors(factors):
    if verbosity > 1:
        for factor in factors:
            print(factor, file = file)


def print_factor(factor):
    if verbosity > 0:
        print(factor, file = file)


def print_simple(text):
    if verbosity > 0:
        print(text, file = file)


def print_groups(query, evidence, barren):
    if verbosity > 0:
        print('Query:', ', '.join(query), file = file)
        print('Evidence:', show_evidence(evidence), file = file)
        print('Barren:', ', '.join(map(str, barren)), '\n', file = file)


def show_evidence(evidence):
    return ', '.join(map(lambda e: f'{e[0]} = {e[1]}', evidence.items()))
