#!/usr/bin/env python3

import unittest
import sys
# Add the parent directory to the path so we can import
# code from our simulator
sys.path.append('../')

from simulator.application import ApplicationGraph
from simulator.topology import TopologyTree
from simulator.schedulers import compact, greedy_pairs

class CompactTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('simple_comm.csv')

    def test_simple_tree(self):
        tree = TopologyTree([4, 2])
        mapping = compact(self.application, tree)
        self.assertEqual(mapping[0], 0)
        self.assertEqual(mapping[1], 1)
        self.assertEqual(mapping[2], 2)
        self.assertEqual(mapping[3], 3)


class GreedyPairsTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('six_tasks.csv')

    def test_greedy(self):
        tree = TopologyTree([4, 2])
        mapping = greedy_pairs(self.application, tree)
        self.assertEqual(mapping[0], 0)
        self.assertEqual(mapping[1], 2)
        self.assertEqual(mapping[2], 3)
        self.assertEqual(mapping[3], 4)
        self.assertEqual(mapping[4], 1)
        self.assertEqual(mapping[5], 5)


if __name__ == '__main__':
    unittest.main()
