"""Simple example.
First part:
- Reads an application from a CSV file, generates a simple tree topology,
  writes a mapping and computes the dilation of said mapping.
Second part:
- Reads a linear topology from a file, and computes the dilation using
the previous mapping
Third part:
- Same problem as the first part, but now uses the greedy_pairs algorithm
for mapping
"""

from simulator.application import ApplicationGraph
from simulator.topology import TopologyTree, Topology
from simulator.support import compute_hopbytes
from simulator.schedulers import greedy_pairs

print('First part: Mapping on a binary tree')
application = ApplicationGraph('inputs/simple_comm.csv')
topology = TopologyTree([2, 2])  # binary tree with four leaves
mapping = [3, 1, 2, 0]
dilation = compute_hopbytes(application, topology, mapping)
print(f'The dilation for the given mapping is equal to {dilation}')

print('Second part: Mapping on a linear topology')
linear = Topology.from_csv('inputs/simple_topo.csv')
dilation = compute_hopbytes(application, linear, mapping)
print(f'The dilation for the given mapping is equal to {dilation}')

print('Third part: Mapping using an algorithm')
mapping = greedy_pairs(application, topology)
dilation = compute_hopbytes(application, topology, mapping)
print(f'The dilation for the given mapping is equal to {dilation}')
