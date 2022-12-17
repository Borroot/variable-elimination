import itertools
import math
import pandas


class Factor:

    uid = 0

    def __init__(self, variables, values):
        assert variables == sorted(variables)

        self.variables = variables
        self.values = values
        self.id = Factor.uid
        Factor.uid += 1


    def _chunk_info(self, variable):
        """
        Give information about a chunk, where a chunk is a grouping of values
        from a domain in a column, possibly of size 1. We provide the number of
        chunks there are for all the values of the given variable, the size of
        these chunks and the space between two chunks.
        """
        # find the index of the variable in the corresponding list
        variable_index = self.variables.index(variable)

        # the number of chunks there are for every variable set
        chunk_num = math.prod(len(variable.domain) for variable in self.variables[:variable_index])

        # the size of the chunks for every variable set
        chunk_size = math.prod(len(variable.domain) for variable in self.variables[variable_index + 1:])

        # the space between two chunks
        jump = chunk_size * (len(variable.domain) - 1)

        return chunk_num, chunk_size, jump


    def marginalize(self, variable):
        """Perform marginalisation on the factor for the given variable."""
        assert variable in self.variables
        assert len(self.variables) > 1

        chunk_num, chunk_size, jump = self._chunk_info(variable)

        # create the new values list
        values = []
        for chunk in range(0, len(self.values), chunk_size + jump):
            for i in range(chunk_size):
                values.append(sum(self.values[chunk + d * chunk_size + i]
                    for d in range(len(variable.domain))))

        # create the new variables list and factor
        variables = [other for other in self.variables if other != variable]
        return Factor(variables, values)


    def reduce(self, variable, value):
        """Perform reduction on the factor for the given variable and value."""
        assert variable in self.variables
        assert value in variable.domain

        chunk_num, chunk_size, jump = self._chunk_info(variable)

        # find the index of the value in the corresponding lists
        value_index = variable.domain.index(value)

        # create the new values list
        values = []
        for chunk in range(chunk_size * value_index, len(self.values), chunk_size + jump):
            for i in range(chunk_size):
                values.append(self.values[chunk + i])

        # create the new variables list and factor
        variables = [other for other in self.variables if other != variable]
        return Factor(variables, values)


    def product(self, other):
        """Compute the product factor of this factor and the given factor."""

        # put the lexicographically lower factor on the left or outside
        factor_order = (self, other) if self.variables < other.variables else (other, self)
        outer_factor = factor_order[0]
        inner_factor = factor_order[1]

        # the masks are used to consider whether two rows should be merged
        outer_mask = [False] * len(outer_factor.variables)
        inner_mask = [False] * len(inner_factor.variables)

        # compute the variables which are in both the factors
        common_variables = []

        for i in range(len(outer_factor.variables)):
            for j in range(len(inner_factor.variables)):
                if outer_factor.variables[i] == inner_factor.variables[j]:
                    common_variables.append(outer_factor.variables[i])
                    outer_mask[i] = True
                    inner_mask[j] = True
        common_variables.sort()

        assert len(common_variables) > 0  # 1 or more variables in common

        # explicitely construct all of the rows for both factors
        outer_rows = list(itertools.product(*map(lambda variable: variable.domain, outer_factor.variables)))
        inner_rows = list(itertools.product(*map(lambda variable: variable.domain, inner_factor.variables)))

        # create the new values list
        values = []
        for outer_index, outer_row in enumerate(outer_rows):
            for inner_index, inner_row in enumerate(inner_rows):
                outer_masked = list(itertools.compress(outer_row, outer_mask))
                inner_masked = list(itertools.compress(inner_row, inner_mask))
                if outer_masked == inner_masked:
                    values.append(outer_factor.values[outer_index] * inner_factor.values[inner_index])

        # create the new variables list and factor
        variables = sorted(list(set(self.variables + other.variables)))
        return Factor(variables, values)


    def __str__(self):
        domains = list(map(lambda variable: variable.domain, self.variables))
        table = []
        for index, row in enumerate(itertools.product(*domains)):
            table.append(list(row) + [self.values[index]])

        df = pandas.DataFrame(table, columns = list(map(str, self.variables)) + ['prob'])
        return str(df) + '\n'

        # builder = ' '.join(map(str, self.variables)) + '\n'
        # domains = list(map(lambda variable: variable.domain, self.variables))
        # for index, row in enumerate(itertools.product(*domains)):
        #     builder += ' '.join(row)
        #     builder += f' {self.values[index]}\n'
        # return builder
