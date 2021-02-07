"""Module containing the representation of the application's
communication graph.

These graphs are assumed to be undirected.
This means that we assume that the affinity of (a,b) is equal to the affinity of (b,a).
The affinity between tasks can be based on the number of messages exchanged,
accesses to the same ranges of memory addresses, volume of data communication,
or others.
"""

import numpy as np


class ApplicationGraph:
    """Representation of an application's communication graph in matrix form

    Attributes
    ----------
    num_tasks : int
        Number of tasks in the application
    affinity : np.ndarray
        Matrix representing the affinity between application tasks

    Raises
    ------
    ValueError
        If the matrix contains NaN, negative values, or it is not square.
    """
    def __init__(self, csv_file=None):
        """Reads the application graph from a CSV file"""
        if csv_file != None:
            self.affinity = np.genfromtxt(csv_file, delimiter=',')
            # Integrity check
            if np.isnan(self.affinity).any():
                print(f"* The communication matrix from file {csv_file} contains NaN values.")
                raise ValueError
            if np.min(self.affinity) < 0.:
                print(f"* The communication matrix from file {csv_file} contains negative values.")
                raise ValueError
            if self.affinity.shape[0] != self.affinity.shape[1]:
                print(f"* The communication matrix from file {csv_file} is not square.")
                raise ValueError
            self.num_tasks = self.affinity.shape[0]
        else:
            self.num_tasks = 1
            self.affinity = np.zeros([1])

    def get_affinity(self, source, dest):
        """Alternative method to get the affinity between two tasks

        Parameters
        ----------
        source : int
            Identifier of the source task
        dest : int
            Identifier of the destination task

        Returns
        -------
        numpy.float64
            Value of the affinity between the two tasks
        """
        return self.affinity[source][dest]

    def max_affinity(self):
        """Returns the maximum affinity value

        Returns
        -------
        numpy.float64
            Maximum affinity value
        """
        return np.max(self.affinity)

    def neighbors(self, task):
        """Finds the neighbors of a given task

        Parameters
        ----------
        task : int
            Source cask identifier

        Returns
        -------
        np.array
            List of task identifiers whose affinity to the source task is not zero
        """
        return np.nonzero(self.affinity[task])[0]
