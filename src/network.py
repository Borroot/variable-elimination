from variable import Variable
from factor import Factor

import pandas as pd


class Network:

    def __init__(self, filename):
        # use the provided network for parsing the .bif file
        self._network = InternalNetwork(filename)

        # create variables with their name and domain
        self.variables = sorted([Variable(name, domain) for name, domain in self._network.values.items()])
        self.variable_names = {variable.name : variable for variable in self.variables}

        # compute the parents and link variables together accordingly
        for variable in self.variables:
            variable.parents = sorted(
                    possible_parent for possible_parent in self.variables
                    if possible_parent.name in self._network.parents[variable.name]
            )

        # compute the children and link variables together accordingly
        for variable in self.variables:
            variable.children = sorted(
                possible_child for possible_child in self.variables
                if variable in possible_child.parents
            )

        # make sure that the columns and the rows are sorted
        for key in self._network.probs.keys():
            self._network.probs[key].sort_index(axis = 1, inplace = True)
            self._network.probs[key].sort_values(by = list(self._network.probs[key].columns), inplace = True)

        # create all the factors
        self.factors = []
        for key in sorted(self._network.probs.keys()):
            variable_names = list(self._network.probs[key].columns[:-1])  # header without 'probs'
            variables = list(map(self.name_to_variable, variable_names))  # actual variables
            values = list(self._network.probs[key][self._network.probs[key].columns[-1]])  # last column
            self.factors.append(Factor(variables, values))


    def variable_to_factor(self, variable):
        """Get the factor corresponding to the given variable."""
        assert variable in self.variables
        return self.factors[self.variables.index(variable)]


    def name_to_factor(self, name):
        """Get the factor corresponding to the given variable name."""
        assert name in map(lambda variable: variable.name, self.variables)
        return self.factors[self.variables.index(self.variable_names[name])]


    def name_to_variable(self, name):
        """Get the variable corresponding to the given variable name."""
        assert name in map(lambda variable: variable.name, self.variables)
        return self.variable_names[name]


class InternalNetwork:
    """
    @Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Bram Pulles

    Representation of a Bayesian network read in from a .bif file.
    This class represents a Bayesian network.
    It can read files in a .bif format (if the formatting is
    along the lines of http://www.bnlearn.com/bnrepository/)

    I made changes so that there is no global class state and I removed the
    SEVEN memory leaks from not closed file descriptors.....
    """


    def __init__(self, filename):
        """
        Construct a bayesian network from a .bif file
        """

        # Possible values per variable
        self.values = {}

        # Parents per variable
        self.parents = {}

        # Probability distributions per variable
        self.probs = {}

        with open(filename, 'r') as file:
            line_number = 0
            for line in file:
                if line.startswith('network'):
                    self.name = ' '.join(line.split()[1:-1])
                elif line.startswith('variable'):
                    self.parse_variable(line_number, filename)
                elif line.startswith('probability'):
                    self.parse_probability(line_number, filename)
                line_number = line_number + 1


    def parse_probability(self, line_number, filename):
        """
        Parse the probability distribution
        """

        lines = None
        with open(filename, 'r') as file:
            lines = file.readlines()

        # get line
        line = lines[line_number]

        # Find out what variable(s) we are talking about
        variable, parents = self.parse_parents(line)
        next_line = lines[line_number + 1].strip()

        # If a variable has no parents, its probabilities start with table
        if next_line.startswith('table'):
            comma_sep_probs = next_line.split('table')[1].split(';')[0].strip()
            probs = [float(p) for p in comma_sep_probs.split(',')]
            df = pd.DataFrame(columns=[variable, 'prob'])
            for value, p in zip(self.values[variable], probs):
                df.loc[len(df)] = [value, p]
                self.probs[variable] = df
        else:
            #create dataFrame to store the variables
            df = pd.DataFrame(columns=[variable] + parents + ['prob'])

            #loop over the lines until a line is the same as "}"
            with open(filename, 'r') as file:
                for i in range(line_number + 1):
                    file.readline()
                for line in file:
                    if '}' in line:
                        # Done reading this probability distribution
                        break

                    # Get the values for the parents
                    comma_sep_values = line.split('(')[1].split(')')[0]
                    values = [v.strip() for v in comma_sep_values.split(',')]

                    # Get the probabilities for the variable
                    comma_sep_probs = line.split(')')[1].split(';')[0].strip()
                    probs = [float(p) for p in comma_sep_probs.split(',')]

                    # Create a row in the df for each value combination
                    for value, p in zip(self.values[variable], probs):
                        df.loc[len(df)] = [value] + values + [p]

            self.probs[variable] = df


    def parse_variable(self, line_number, filename):
        """
        Parse the name of a variable and its possible values
        """
        lines = None
        with open(filename, 'r') as file:
            lines = file.readlines()

        variable = lines[line_number].split()[1]
        line = lines[line_number+1]
        start = line.find('{') + 1
        end = line.find('}')
        values = [value.strip() for value in line[start:end].split(',')]
        self.values[variable] = values


    def parse_parents(self, line):
        """
        Find out what variables are the parents
        Returns the variable and its parents
        """
        start = line.find('(') + 1
        end = line.find(')')
        variables = line[start:end].strip().split('|')
        variable = variables[0].strip()
        if len(variables) > 1:
            parents = variables[1]
            self.parents[variable] = [v.strip() for v in parents.split(',')]
        else:
            self.parents[variable] = []
        return variable, self.parents[variable]
