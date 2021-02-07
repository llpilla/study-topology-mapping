#!/usr/bin/env python3

import unittest
import sys
# Add the parent directory to the path so we can import
# code from our simulator
sys.path.append('../')

from simulator.application import ApplicationGraph
from simulator.topology import TopologyTree
from simulator.schedulers import scatter, greedy_pairs_with_topology, eagermap
from simulator.support import compute_hopbytes

class ScatterTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('six_tasks.csv')

    def test_simple_tree(self):
        tree = TopologyTree([4, 2])
        mapping = scatter(self.application, tree)
        self.assertEqual(mapping[0], 0)
        self.assertEqual(mapping[1], 4)
        self.assertEqual(mapping[2], 2)
        self.assertEqual(mapping[3], 6)
        self.assertEqual(mapping[4], 1)
        self.assertEqual(mapping[5], 5)


class GreedyPairsWithTopologyTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('six_tasks.csv')

    def test_greedy(self):
        tree = TopologyTree([2, 3])
        mapping = greedy_pairs_with_topology(self.application, tree)
        self.assertEqual(mapping[0], 0)
        self.assertEqual(mapping[1], 3)
        self.assertEqual(mapping[2], 4)
        self.assertEqual(mapping[3], 2)
        self.assertEqual(mapping[4], 1)
        self.assertEqual(mapping[5], 5)


class EagerMapTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('six_tasks.csv')

    def test_eager(self):
        tree = TopologyTree([2, 2, 2])
        mapping = eagermap(self.application, tree)
        dilation = compute_hopbytes(self.application, tree, mapping)
        # expected pairs: (0,4), (1,2), (3,5), artificial (6,7)
        # expected pair of pairs: ((1,2),(3,5)), ((0,4),(6,7))
        expected_dilation = (5*6+7*2+1*6) + (4*2+3*4+4*4) + (1*4+3*4) + (2*2) + (9*6)
        self.assertTrue(dilation < expected_dilation + 1)


if __name__ == '__main__':
    unittest.main()
