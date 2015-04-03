u"""
Modelise un reseau compose uniquement de variables discretes.
"""


class Distribution():
    def __init__(self, probabilities):
        self.probabilities = probabilities

    def normalize(self):
        total = sum(self.get_probabilities())
        self.probabilities = [prob / total for prob in self.probabilities]
        return self

    def set_probability(self, index, probability):
        assert 0 <= index < len(self.probabilities)
        assert 0. <= probability <= 1.
        self.probabilities[index] = probability
        return self

    def get_probabilities(self):
        return self.probabilities[:]

    def get_probability(self):
        return self.probabilities[0]


__author__ = 'plperron'
