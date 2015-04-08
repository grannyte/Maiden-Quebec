"""
Modelise les operateurs necessaires lors de requetes sur un reseau bayesien.
Les 3 classes _Affectation, Query et Evidence sont identiques.
Ici, ils different pour clarifier la semantique
"""


class _Affectation(object):
    def __init__(self, variable_name, domain_value):
        self.variable_name = variable_name
        self.domain_value = domain_value

    def get_variable_name(self):
        return self.variable_name

    def get_domain_value(self):
        return self.domain_value


class Query(_Affectation):
    def __init__(self, variable_name, domain_value):
        super(Query, self).__init__(variable_name, domain_value)


class Evidence(_Affectation):
    def __init__(self, variable_name, domain_value):
        super(Evidence, self).__init__(variable_name, domain_value)

    def is_evidence_of(self, variable):
        if variable.get_name() != super(Evidence, self).get_variable_name():
            return False
        for domain in variable.get_domains():
            if domain == super(Evidence, self).get_domain_value():
                return True
        return False


class Proposition():
    def __init__(self, query, evidences):
        self.query = query
        self.evidences = evidences

    def get_query(self):
        return self.query

    def get_evidences(self):
        return self.evidences[:]


__author__ = 'plperron'
