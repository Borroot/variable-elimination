def print_header(text):
    print('-----------------------------------------------------')
    print(text)
    print('-----------------------------------------------------\n')


def print_factors_brief(factors):
    for factor in factors:
        print(factor.brief())
    print()


def print_factors(factors):
    for factor in factors:
        print(factor)


def print_groups(query, evidence, barren):
    print('Query:', ', '.join(query))
    print('Evidence:', show_evidence(evidence))
    print('Barren:', ', '.join(map(str, barren)), '\n')


def show_evidence(evidence):
    return ', '.join(map(lambda e: f'{e[0]} = {e[1]}', evidence.items()))
