class DiscreteBayesianNetwork:
    def __init__(self, vars):
        self.vars = vars

    def get_variable_by_name(self, name):
        return self.vars[name]

    def infer(self, proposition, inference):
        return inference.infer(proposition.get_query(), proposition.get_evidences(), self)

    def get_variable_in_topological_order(self):
        sorted_vars = [v for k, v in self.vars.iteritems()]
        return sorted(sorted_vars, key=lambda var: var.height())


__author__ = 'plperron'
