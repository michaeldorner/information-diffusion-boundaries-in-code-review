# Upper Bound of Information Diffusion in Code Review: Replication package

[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)

Simulation code for the study "Upper Bound of Information Diffusion in Code Review"

## Introduction

The underlying idea of our in-silico experiment is simple: We simulate an artificial information diffusion process in empirical communication networks emerging from code review and measure the minimal paths among all participants, the upper bound of information diffusion. The cardinality of reachable participants indicates how far (RQ 1) and minimal distances between participants indicate fast (RQ 2) information can spread following the communication channels that code review provide under best-case assumptions.

Yet, since communication, and, therefore, information diffusion, is (1) inherently a time-dependent process that is (2) not necessarily bilateral—often more than two participants exchange information in a code review—, traditional graphs are not capable of rendering information diffusion without dramatically overestimate information diffusion [(Dorner et al. 2022)](https://dl.acm.org/doi/abs/10.1145/3544902.3546254). Therefore, we use time-varying hypergraphs to model the communication network and measure the minimal paths of all vertices. Since a hypergraph is a generalization of a traditional graph, traditional graph algorithms (i.e., Dijkstra's algorithm) for determining minimal paths can be used.

The connotation of minimal is two-fold in time-varying hypergraphs: A distance in time-varying hypergraphs between two vertices can be topological or temporal. This means a minimal path in time-varying hypergraphs can be the _shortest_, _fastest_, and _foremost_ distance between vertices. Those different notions of a minimal path enable us to understand how fast and how far information can spread through code review.

For more details on time-varying hypergraphs in general and modelling communication networks that emerges from code review with time-varying hypergraphs, have a look into [(Dorner et al. 2022)](https://dl.acm.org/doi/abs/10.1145/3544902.3546254)

## Installation

The simulation requires Python 3.10 and higher. Due to the [significant performance improvements in Python 3.11](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-faster-cpython) and the heavy CPU workload in the simulation, Python 3.11 is highly recommended!

The project depends on only three external libraries: [`tqdm`](https://github.com/tqdm/tqdm) and [`pandas`](https://pandas.pydata.org). Install via

```
python3 -m pip install -r requirements.txt
```

## Usage

To run the full simulation, use

```
python3 -m simulation.run
```

Please notice that depending on your hardware, the complete simulation may run several days and max out the CPU power. On a Apple MacBook M1 Max, it takes about two days to complete. The simulations is highly parallelized which means: The more cores, the better/faster.

The simulation provides options

- `--select <name 1> <name 2> ...` to select a subset of available code review networks
- `--vertex_dijkstra` to use a vertex-based implementation of Dijkstra's algorithm (which tends to be slower),
- `--num_processes` to limit the number of processes

For an overview of all options, use `python3 -m simulation.run --help`.

The code review communication networks are in the subfolder `data/networks`, the simulation results are stored in `data/minimal_paths`

## Tests and verification

### Testing

So far, the simulation provides only a rudimentary test setup. You can run all tests via

```
pip3 -m unittest discover
```

### Verification

To verify the results, run

```
shasum -a 256 data/minimal_paths/*                      
```

and compare the hash values of our results:

```
d455f1e37237014830fa9aaca76232594c92c193c241b71ca28ec69969163daf  data/minimal_paths/microsoft.pickle
d455f1e37237014830fa9aaca76232594c92c193c241b71ca28ec69969163daf  data/minimal_paths/microsoft.csv
```

## Visualization

Because of the large runtime of the simulation, we provide precomputed results of the simulation via [Zenodo](). You can download the results and place the `.pickle` and `.csv` files in the subfolder `data/minimal_paths`. Consider verify the `.pickle` and `.csv` files (see [Verification](#verification)).

To visualize the results and reproduce the tables and figures of the publication, see the Jupyter notebooks in the subfolder `notebooks/`.

## Credits

## License

Copyright © 2023 Michael Dorner

This work is licensed under [MIT license](LICENSE).
