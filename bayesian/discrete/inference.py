from bayesian.proposition import Evidence


class Inference(object):
    def infer(self, query, evidences, bn):
        pass


class EnumerationAsk():
    def __init__(self):
        pass

    def infer(self, query, evidences, bn):
        # Q = a distribution over X, where Q(xi) is P(X=xi)
        distribution = bn.get_variable_by_name(query.get_variable_name()).calc_probabilities()
        # for each value xi that X can have do
        evidences = evidences[:]
        evidences.append(None)
        topological_vars = bn.get_variable_in_topological_order()
        domains = bn.get_variable_by_name(query.get_variable_name()).get_domains()
        for d in range(0, len(domains)):
            # Q(xi) = ENUMERATE-ALL(bn.VARS, e_xi), where e_xi is the evidence e plus the assignment X=xi
            evidences[len(evidences) - 1] = Evidence(query.get_variable_name(), domains[d])
            distribution.set_probability(d, self.__enumerate_all(topological_vars, evidences))
        # return NORMALIZE(Q)
        return bn.get_variable_by_name(query.get_variable_name()).get_probability_from(distribution.normalize(),
            query.get_domain_value())

    def __enumerate_all(self, topological_vars, evidences):
        # if EMPTY(vars) then return 1.0
        if len(topological_vars) == 0:
            return 1.
        # Y = FIRST(vars)
        first = topological_vars[0]
        topological_vars = topological_vars[1:]
        # if Y is assigned a value (call it y) in e then
        if self.__is_assigned(first, evidences):
            return first.calcProbabilities(evidences).get_probability() * \
                   self.__enumerate_all(topological_vars, evidences)
        else:
            evidences = evidences[:]
            evidences.append(None)
            somme = 0.
            for domain in first.get_domains():
                evidences[len(evidences) - 1] = Evidence(first.get_name(), domain)
                somme += first.calcProbabilities(evidences).get_probability() * \
                         self.__enumerate_all(topological_vars, evidences)
            return somme

    def __is_assigned(self, var, evidences):
        for evidence in evidences:
            if evidence.is_evidence_of(var):
                return True
        return False


class EliminationAsk():
    def __init__(self):
        pass

    def infer(self, query, evidences, bn):
        pass


__author__ = 'plperron'
