"""Module containing a representation of the machine topology graph."""

import numpy as np
from operator import mul
from functools import reduce


class Topology:
    """Machine topology represented as a matrix of distances

    Attributes
    ----------
    num_cores : int
        Number of cores in the machine topology
    distances : np.ndarray
        Matrix representing the distance between cores

    Raises
    ------
    ValueError
        If the matrix contains NaN, negative values, or it is not square
    """
    def __init__(self, distances):
        self.distances = np.array(distances)
        # Integrity check
        if np.isnan(self.distances).any():
            print("* The distances matrix contains NaN values.")
            raise ValueError
        if np.min(self.distances) < 0.:
            print("* The distances matrix contains negative values.")
            raise ValueError
        if self.distances.shape[0] != self.distances.shape[1]:
            print("* The distances matrix is not square.")
            raise ValueError
        self.num_cores = self.distances.shape[0]

    def get_hops_between_cores(self, first_core, second_core):
        """Computes the distance in number of hops between two cores

        Parameters
        ----------
        first_core : int
            Identifier of a core
        second_core : int
            Identifier of a core

        Returns
        -------
        int
            Number of hops (edges) between the two cores

        Raises
        ------
        ValueError
            If a core is outside the range of cores in the topology
        """
        if (first_core < self.num_cores) and (second_core < self.num_cores):
            return self.distances[first_core][second_core]
        else:
            print(f"* Requiring distances for cores {first_core} and {second_core} when only {self.num_cores} cores are available")
            raise ValueError

    @staticmethod
    def from_csv(csv_file):
        """Reads a machine topology matrix from a CSV file

        Parameters
        ----------
        csv_file : string
            File containing the matrix of distances between cores

        Returns
        -------
        Topology object
            Machine topology read from file
        """
        distances = np.genfromtxt(csv_file, delimiter=',')
        topology = Topology(distances)
        return topology


class TopologyTree(Topology):
    """Machine topology represented as a tree.

    Attributes
    ----------
    num_cores : int
        Number of cores in the machine topology
    num_levels : int
        Number of levels in the tree. Minimum = 2 (root and cores)
    arity : list of int
        Arity (number of children) for nodes at each level of the tree
    parents : list of list of int
        Index of the parents of nodes at each level of the tree (except the root)

    Notes
    -----
    Level 0 in the tree represents the root, while level 'num_levels - 1'
    represents the cores.
    """
    def __init__(self, arity):
        self.num_cores = reduce(mul, arity)
        self.num_levels = len(arity) + 1
        self.arity = arity
        # Starts the list of parents by creating empty levels
        parents = [[] for i in range(self.num_levels)]
        # Creates a dummy parent for the root
        parents[0].append(0)
        # Iterates creating the parent lists for the next levels
        for level in range(1, self.num_levels):
            # For all possible parents of this level
            for parent in range(len(parents[level - 1])):
                # Adds the nodes pointing to said parent
                parents[level].extend([parent] * arity[level-1])
        self.parents = parents

    def get_level_arity(self, level):
        """Returns the arity of a given level in the topology above the cores

        Parameters
        ----------
        level : int
            Level in the machine topology

        Returns
        -------
        int
            Arity of the level

        Raises
        ------
        ValueError
            If the level in the topology does not exist
        """
        if level < self.num_levels - 1:
            return self.arity[level]
        else:
            print(f"* Requiring arity of level {level} when only {self.num_levels-1} is available")
            raise ValueError

    def get_level_size(self, level):
        """Returns the number of nodes in a given level of the topology

        Parameters
        ----------
        level : int
            Level in the machine topology

        Returns
        -------
        int
            Number of nodes in the level

        Raises
        ------
        ValueError
            If the level in the topology does not exist
        """
        if level < self.num_levels:
            return len(self.parents[level])
        else:
            print(f"* Requiring number of nodes for level {level} when only {self.num_levels} are available")
            raise ValueError

    def get_level_parents(self, level):
        """Returns the list of parents for a given level of the topology

        Parameters
        ----------
        level : int
            Level in the machine topology

        Returns
        -------
        list of int
            Parents of nodes in the level

        Raises
        ------
        ValueError
            If the level in the topology does not exist
        """
        if level < self.num_levels:
            return self.parents[level]
        else:
            print(f"* Requiring number of nodes for level {level} when only {self.num_levels} are available")
            raise ValueError

    def get_distance(self, first_node, second_node, level):
        """Computes the distance in number of hops between two nodes in the tree

        Parameters
        ----------
        first_node : int
            Identifier of a node
        second_node : int
            Identifier of a node
        level : int
            Level in the tree

        Returns
        -------
        int
            Number of hops (edges) between the two nodes

        Raises
        ------
        ValueError
            If the level in the topology does not exist
        """
        if level < self.num_levels:
            if first_node == second_node:
                return 0
            else:
                parent_first = self.parents[level][first_node]
                parent_second = self.parents[level][second_node]
                return 2 + self.get_distance(parent_first, parent_second, level - 1)
        else:
            print(f"* Requiring distances at level {level} when only {self.num_levels} are available")
            raise ValueError

    def get_hops_between_cores(self, first_core, second_core):
        """Computes the distance in number of hops between two cores

        Parameters
        ----------
        first_core : int
            Identifier of a core
        second_core : int
            Identifier of a core

        Returns
        -------
        int
            Number of hops (edges) between the two cores

        Raises
        ------
        ValueError
            If a core is outside the range of cores in the topology
        """
        if (first_core < self.num_cores) and (second_core < self.num_cores):
            return self.get_distance(first_core, second_core, self.num_levels - 1)
        else:
            print(f"* Requiring distances for cores {first_core} and {second_core} when only {self.num_cores} cores are available")
            raise ValueError
