"""Module containing topology mapping algorithms

Implemented scheduling algorithms: compact
Methods with interfaces but no implementation:
"""

import copy


def compact(application, topology):
    """Computes a compact, round-robin distribution of tasks over cores

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph

    Returns
    -------
    list of int
        Mapping of tasks to cores
    """
    num_tasks = application.num_tasks
    num_cores = topology.num_cores
    mapping = [i % num_cores for i in range(num_tasks)]
    return mapping

def greedy_pairs(application, topology):
    """Computes a greedy mapping by putting tasks with high affinity in consecutive cores

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph

    Returns
    -------
    list of int
        Mapping of tasks to cores
    """
    # Creates a starting empty mapping
    mapping = [None for i in range(application.num_tasks)]
    # Next core to map tasks
    next_core = 0
    # Makes a copy of the application graph to be able to change its values
    app = copy.deepcopy(application)

    # Iterates over all tasks to map them in pairs
    for i in range(application.num_tasks):
        if mapping[i] != None:
            continue  # Nothing to do for a task that has already been mapped
        # Maps the task
        mapping[i] = next_core
        next_core = (next_core + 1) % topology.num_cores
        # Finds a task that communicates the most with task i
        most_comm = app.affinity[i].argmax()
        # Changes the affinity between these tasks so it does not come up anymore
        app.affinity[:,i] = -1
        app.affinity[:,most_comm] = -1
        # Makes sure that the highest affinity is happening with another task
        # (issues could happen if every other task has been mapped already,
        # or if the task has zero affinity with other unmapped tasks)
        if i != most_comm:
            mapping[most_comm] = next_core
            next_core = (next_core + 1) % topology.num_cores
    # returns the solution
    return mapping


def scatter(application, topology):
    """Computes a scattered distribution of tasks over cores

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph

    Returns
    -------
    list of int
        Mapping of tasks to cores
    """
    # TODO


def greedy_pairs_with_topology(application, topology):
    """Computes a greedy mapping by putting tasks with high affinity in cores
    that have the smallest distances

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph

    Returns
    -------
    list of int
        Mapping of tasks to cores
    """
    # TODO


def eagermap(application, topology):
    """Mapping tasks on a hierarchical topology following the EagerMap algorithm

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph

    Returns
    -------
    list of int
        Mapping of tasks to cores

    Notes
    -----
    The algorithm is described in
    Eduardo H.M. Cruz, Matthias Diener, Laércio L. Pilla, and Philippe O.A. Navaux.
    "EagerMap: A task mapping algorithm to improve communication and load balancing
    in clusters of multicore systems." ACM Transactions on Parallel Computing (TOPC)
    5, no. 4 (2019): 1-24.
    """
    # TODO
