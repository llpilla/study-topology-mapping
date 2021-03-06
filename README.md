# Practical topology mapping activity

This repository is intended for use by students to practice concepts related to topology mapping and notions of locality metrics (dilation).
It contains a few scheduling algorithms and some support functions.
A set of activities using this repository is presented in the [activities section](#activities) below.

## How To

- The code in this repository is written using Python3 and a few of its modules.
In order to check and install any missing modules, run `python3 setup.py`

- To run a code example, try `python3 example.py`.

- To learn more about the schedulers and support functions, try the code below in your Python3 interpreter:

```python
>>> import simulator.schedulers as schedulers
>>> help(schedulers)
>>> import simulator.application as application
>>> help(application)
```

- To check if the code you downloaded or changed is still working properly, try the following commands:

```bash
$ cd unitary_tests
$ ./test_implemented_schedulers.py 
$ ./test_support.py
```

- To check if the new schedulers you have implemented are working as intended, try the following commands:

```bash
$ cd unitary_tests
$ ./test_other_schedulers.py 
```

## Activities

**Basic steps**

1. Run `python3 example.py` and try to understand its results. Check how to write code to use this simple simulator. Change it to display any information that you feel is relevant.

2. Write the scatter scheduler (complete function *scatter* in [the schedulers file](simulator/schedulers.py)). Check if it passes the tests in [the unitary tests' file](unitary_tests/test_other_schedulers.py).

3. Try to generate and run some tests comparing the gather and scatter algorithms. Compare how they perform based on the dilation (*hop-bytes*) metric. Other communication matrices can be found [here](https://github.com/unibas-dmi-hpc/MapLib/tree/master/mapping-matters-commMatrices).

4. Write the greedy pairs with topology scheduler. Check if it passes the tests in the unitary tests' file.

5. Try to generate and run some tests comparing the new algorithm to the greedy pairs algorithm. Evaluate if the added topology information has some impact in the dilation of the mapping.

**Additional challenge**

6. Write the [EagerMap](https://hal.archives-ouvertes.fr/hal-02062952/document) scheduler and check if it passes the tests in the unitary tests' file. Compare its mapping with the ones generated by the greedy algorithms.

7. Write your own scheduler, or try to implement a known scheduler from the state of the art (for instance, [TreeMatch](https://www.labri.fr/perso/ejeannot/publications/europar10.pdf)). Compare its mapping to the ones generated by some of the previous algorithms.
