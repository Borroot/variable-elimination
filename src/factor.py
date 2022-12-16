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


    def reduce(self, variable, value):
        assert variable in self.variables
        assert value in variable.domain

        # find the index of the variable and the value in the corresponding lists
        variable_index = self.variables.index(variable)
        value_index = variable.domain.index(value)

        # the number of chunks there are for every variable set
        chunk_num = math.prod(len(variable.domain) for variable in self.variables[:variable_index])

        # the size of the chunks for every variable set
        chunk_size = math.prod(len(variable.domain) for variable in self.variables[variable_index + 1:])

        # the space between two chunks
        jump = chunk_size * (len(variable.domain) - 1)

        # create the new values list
        values = []
        for chunk in range(chunk_size * variable_index, len(self.values), chunk_size + jump):
            print(chunk)
            for i in range(0, chunk_size):
                values.append(self.values[chunk + i])

        # create the new variables list and factor
        variables = [other for other in self.variables if other != variable]
        return Factor(variables, values)

        print(chunk_num, chunk_size, jump)


    def __str__(self):
        domains = list(map(lambda variable: variable.domain, self.variables))
        table = []
        for index, row in enumerate(itertools.product(*domains)):
            table.append(list(row) + [self.values[index]])

        df = pandas.DataFrame(table, columns = list(map(str, self.variables)) + ['prob'])
        return str(df)

        # builder = ' '.join(map(str, self.variables)) + '\n'
        # domains = list(map(lambda variable: variable.domain, self.variables))
        # for index, row in enumerate(itertools.product(*domains)):
        #     builder += ' '.join(row)
        #     builder += f' {self.values[index]}\n'
        # return builder
