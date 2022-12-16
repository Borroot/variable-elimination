from functools import total_ordering


@total_ordering
class Variable:

    def __init__(self, name, domain):
        self.name = name
        self.domain = sorted(domain)
        self.parents = None
        self.children = None


    def __lt__(self, other):
        return self.name < other.name


    def __eq__(self, other):
        return self.name == other.name


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.__str__()
