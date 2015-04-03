u"""
Modelise une variable discrete d'un reseau bayesien.
"""

from distribution import Distribution


class RandomVariable():
    def __init__(self, name, parents, domains, distribution):
        self.name = name
        self.parents = parents
        self.__domains = domains
        self.distribution = distribution

    def get_name(self):
        return self.name

    def get_domains(self):
        return self.__domains[:]

    def get_probability_from(self, distribution, domain):
        probabilities = distribution.get_probabilities()
        assert len(probabilities) == len(self.__domains)
        indexes = [d for d in range(0, len(self.__domains)) if self.__domains[d] == domain]
        assert len(indexes) == 1
        return probabilities[indexes[0]]

    def height(self):
        """La hauteur se definit par le nombre de parents, grand-parents...etc"""
        maximum = 0.
        for parent in self.parents:
            maximum = max(maximum, parent.height())
        return 1 + maximum

    def calcProbabilities(self, evidences):
        """
        Elage les evidences excedentaires et calcule la probabilite selon les evidences pertinentes restantes
        :param evidences:
        :return:
        """
        topological_evidences = self.__sort_by_topological_order(evidences)
        topological_variables = self.parents[:]
        topological_variables.append(self)
        assert len(topological_variables) == len(topological_evidences)
        probabilitites = self.distribution.get_probabilities()
        start, count = 0, len(probabilitites)
        for i in range(0, len(topological_evidences)):
            domains = topological_variables[i].get_domains()
            for d in range(0, len(domains)):
                if domains[d] == topological_evidences[i].get_domain_value():
                    start += count / len(domains) * d
                    count /= len(domains)
                    break
        assert count == 1
        return Distribution(probabilitites[start: start + count])

    def __sort_by_topological_order(self, evidences):
        topological_evidences = [None] * (len(self.parents) + 1)
        i = 0
        for parent in self.parents:
            for evidence in evidences:
                if parent.get_name() == evidence.get_variable_name():
                    topological_evidences[i] = evidence
                    i += 1
                    break
        for evidence in evidences:
            if evidence.get_variable_name() == self.get_name():
                topological_evidences[i] = evidence
                i += 1
                break
        assert i == len(topological_evidences)
        return topological_evidences

    def calc_probabilities(self):
        probabilities = self.distribution.get_probabilities()
        domain_probabilities = [0.] * len(self.get_domains())
        for d in range(0, len(self.get_domains())):
            for p in range(d, len(probabilities), len(self.get_domains())):
                domain_probabilities[d] += probabilities[p]
        return Distribution(domain_probabilities).normalize()


__author__ = 'plperron'
