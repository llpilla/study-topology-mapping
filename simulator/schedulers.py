"""Module containing topology mapping algorithms

Implemented scheduling algorithms: compact
Methods with interfaces but no implementation:
"""

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


