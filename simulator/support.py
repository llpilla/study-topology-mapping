"""Module containing a representation of the machine topology graph."""


def compute_hopbytes(application, topology, mapping):
    """Computes the hopbytes based on the application and topology graphs, and a mapping of application tasks to topology cores

    Parameters
    ----------
    application : ApplicationGraph object
        Application's communication graph
    topology : Topology object
        Machine topology graph
    mapping : list of int
        Mapping of tasks to cores

    Returns
    -------
    numpy.float64
        Sum of hopbytes for the mapping

    Raises
    ------
    ValueError
        If the size of the mapping does not match the number of tasks in the application,
        or any tasks are mapped to cores that do not exist.
    """
    # Checking for problems before starting
    if len(mapping) != application.num_tasks:
        raise ValueError
    if (min(mapping) < 0) or (max(mapping) >= topology.num_cores):
        raise ValueError
    # Compute the dilation (hop-bytes) for the mapping
    dilation = 0
    num_tasks = len(mapping)
    # For all tasks
    for source in range(num_tasks):
        for dest in application.neighbors(source):
            if dest > source:  # check to avoid counting interactions twice
                affinity = application.get_affinity(source, dest)
                distance = topology.get_hops_between_cores(mapping[source], mapping[dest])
                dilation += affinity * distance
    return dilation
