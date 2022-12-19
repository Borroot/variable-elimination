import itertools
import math
import pandas


class Factor:

    uid = 0

    def __init__(self, variables, values, reduced = []):
        assert variables == sorted(variables)

        self.variables = variables
        self.values = values
        self.reduced = reduced  # all variables that got reduced

        self.id = Factor.uid
        Factor.uid += 1


    def clone(self):
        return Factor(self.variables, self.values.copy())


    def normalize(self):
        total = sum(self.values)
        values = [value / total for value in self.values]
        return Factor(self.variables, values, self.reduced.copy())


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
        return Factor(variables, values, self.reduced.copy())


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
        return Factor(variables, values, self.reduced.copy() + [variable])


    def _product_reduced(reduced_factor, factor):
        """Compute the product when at least one factor is completely reduced."""
        values = list(map(lambda value: value * reduced_factor.values[0], factor.values))
        reduced = sorted(list(set(reduced_factor.reduced.copy() + factor.reduced.copy())))
        return Factor(factor.variables.copy(), values, reduced)


    def product(self, othr):
        """Compute the product factor of this factor and the given factor."""

        # simplify if at least one of the factors is completely reduced
        if len(self.variables) == 0:
            return Factor._product_reduced(self, othr)
        if len(othr.variables) == 0:
            return Factor._product_reduced(othr, self)

        # the factors need to have at least one factor in common
        assert len(set(self.variables) & set(othr.variables)) > 0

        # create the final product table entries without the probabilities
        variables = sorted(list(set(self.variables + othr.variables)))
        rows = list(itertools.product(*map(lambda variable: variable.domain, variables)))

        # the masks are used to get an assignment for indexing the factors
        mask_self = [variable in self.variables for variable in variables]
        mask_othr = [variable in othr.variables for variable in variables]

        # convert an ordered assignment of values to an index in the factor
        def assignment_to_index(factor, assignment):
            index = 0
            size = 1
            for i in range(len(factor.variables) - 1, -1, -1):
                index += size * factor.variables[i].domain.index(assignment[i])
                size *= len(factor.variables[i].domain)
            return index

        # create the new values list
        values = []
        for row in rows:
            # get the value assignments, i.e. the rows for the factor tables
            assignment_self = list(itertools.compress(row, mask_self))
            assignment_othr = list(itertools.compress(row, mask_othr))

            # assignment to index in factors
            index_self = assignment_to_index(self, assignment_self)
            index_othr = assignment_to_index(othr, assignment_othr)

            # calculate the new value
            value = self.values[index_self] * othr.values[index_othr]
            values.append(value)

        # create the combined reduced list and factor
        reduced = sorted(list(set(self.reduced.copy() + othr.reduced.copy())))
        return Factor(variables, values, reduced)


    def brief(self):
        variables = ', '.join(map(str, self.variables))
        reduced = ', '.join(map(str, self.reduced))
        return f'f{self.id:02}({variables})({reduced})'


    def __str__(self):
        domains = list(map(lambda variable: variable.domain, self.variables))
        table = []
        for index, row in enumerate(itertools.product(*domains)):
            table.append(list(row) + [self.values[index]])

        table = str(pandas.DataFrame(table, columns = list(map(str, self.variables)) + ['prob']))
        table = f'f{self.id:02}, variables: {self.variables}, reduced: {self.reduced}\n{table}\n'
        return table
