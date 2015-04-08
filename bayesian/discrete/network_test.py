import unittest

from network import DiscreteBayesianNetwork
from distribution import Distribution
from variable import RandomVariable
from bayesian.proposition import *
from inference import EnumerationAsk


class BayesianNetworkTestCase(unittest.TestCase):
    def setUp(self):
        name = "burglar"
        domains = ["false", "true"]
        parents = []
        distribution = Distribution([.999, .001])
        burglar = RandomVariable(name, parents, domains, distribution)
        name = "earthquake"
        domains = ["false", "true"]
        parents = []
        distribution = Distribution([.998, .002])
        earthquake = RandomVariable(name, parents, domains, distribution)
        name = "alarm"
        domains = ["false", "true"]
        parents = [burglar, earthquake]
        distribution = Distribution([.999, .001, .71, .29, .06, .94, .05, .95])
        alarm = RandomVariable(name, parents, domains, distribution)
        name = "john"
        domains = ["false", "true"]
        parents = [alarm]
        distribution = Distribution([.95, .05, .1, .9])
        john = RandomVariable(name, parents, domains, distribution)
        name = "mary"
        domains = ["false", "true"]
        parents = [alarm]
        distribution = Distribution([.99, .01, .3, .7])
        mary = RandomVariable(name, parents, domains, distribution)
        vars = {"burglar": burglar, "earthquake": earthquake, "alarm": alarm, "john": john, "mary": mary}
        self.bn = DiscreteBayesianNetwork(vars)

    def test_infer_simple(self):
        evidences = []
        proposition = Proposition(Query("burglar", "false"), evidences)
        actual = self.bn.infer(proposition, EnumerationAsk())
        expect = .999
        self.assertEqual(expect, actual)

    def test_infer_simple2(self):
        evidences = []
        proposition = Proposition(Query("burglar", "true"), evidences)
        actual = self.bn.infer(proposition, EnumerationAsk())
        expect = .001
        self.assertEqual(expect, actual)

    def test_infer_russel_norvig_burglar_example(self):
        evidences = [Evidence("john", "true"), Evidence("mary", "true")]
        proposition = Proposition(Query("burglar", "true"), evidences)
        actual = self.bn.infer(proposition, EnumerationAsk())
        expect = .2841718353643929
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()

__author__ = 'plperron'
