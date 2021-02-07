#!/usr/bin/env python3

import unittest
import sys
# Add the parent directory to the path so we can import
# code from our simulator
sys.path.append('../')

from simulator.application import ApplicationGraph
from simulator.topology import TopologyTree, Topology
from simulator.support import compute_hopbytes


class DilationTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationGraph('simple_comm.csv')

    def test_simple_tree(self):
        topology = TopologyTree([4])
        mapping = [0, 1, 2, 3]
        dilation = compute_hopbytes(self.application, topology, mapping)
        self.assertEqual(dilation, 24)

    def test_bin_tree(self):
        topology = TopologyTree([2, 2])
        mapping = [0, 1, 2, 3]
        dilation = compute_hopbytes(self.application, topology, mapping)
        self.assertEqual(dilation, 32)

    def test_very_far(self):
        topology = TopologyTree([2, 2, 2, 2, 2, 2])
        mapping = [0, 63, 3, 61]
        dilation = compute_hopbytes(self.application, topology, mapping)
        self.assertEqual(dilation, 144)

    def test_together(self):
        topology = TopologyTree([2, 2, 2, 2, 2, 2])
        mapping = [0, 0, 0, 0]
        dilation = compute_hopbytes(self.application, topology, mapping)
        self.assertEqual(dilation, 0)

    def test_topology(self):
        topology = Topology([[0, 2, 2, 2],[2, 0, 1, 4],[2, 1, 0, 3],[2, 4, 3, 0]])
        mapping = [0, 1, 2, 3]
        dilation = compute_hopbytes(self.application, topology, mapping)
        self.assertEqual(dilation, 2*2+1*4+6*3)


if __name__ == '__main__':
    unittest.main()
