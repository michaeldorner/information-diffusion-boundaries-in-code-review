# Upper Bound of Information Diffusion in Code Review: Replication package

[![GitHub](https://img.shields.io/github/license/michaeldorner/information-diffusion-boundaries-in-code-review)](./LICENSE)
[![GitHub Actions](https://github.com/michaeldorner/information-diffusion-boundaries-in-code-review/actions/workflows/test.yml/badge.svg)](https://img.shields.io/github/actions/workflow/status/michaeldorner/information-diffusion-boundaries-in-code-review/main.yml)
[![Codacy Badge](https://img.shields.io/codacy/grade/ef43d5d9b7c74ec0b211c03d91c448d8)](https://app.codacy.com/gh/michaeldorner/information-diffusion-boundaries-in-code-review/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://img.shields.io/codacy/coverage/ef43d5d9b7c74ec0b211c03d91c448d8)](https://app.codacy.com/gh/michaeldorner/information-diffusion-boundaries-in-code-review/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7898863.svg)](https://doi.org/10.5281/zenodo.7898863)

Simulation code for the study "Upper Bound of Information Diffusion in Code Review"


## Introduction

The underlying idea of our in-silico experiment is simple: We simulate an artificial information diffusion process in empirical communication networks emerging from code review and measure the minimal paths among all participants, the upper bound of information diffusion. The cardinality of reachable participants indicates how far (RQ 1) and minimal distances between participants indicate fast (RQ 2) information can spread following the communication channels that code review provide under best-case assumptions.

Yet, since communication, and, therefore, information diffusion, is (1) inherently a time-dependent process that is (2) not necessarily bilateral—often more than two participants exchange information in a code review—, traditional graphs are not capable of rendering information diffusion without dramatically overestimate information diffusion [(Dorner et al. 2022)](https://dl.acm.org/doi/abs/10.1145/3544902.3546254). Therefore, we use time-varying hypergraphs to model the communication network and measure the minimal paths of all vertices. Since a hypergraph is a generalization of a traditional graph, traditional graph algorithms (i.e., Dijkstra's algorithm) for determining minimal distances between vertices can be used.

The connotation of minimal is two-fold in time-varying hypergraphs: A distance in time-varying hypergraphs between two vertices can be topological or temporal. This means a minimal path in time-varying hypergraphs can be the _shortest_, _fastest_, and _foremost_ distance between vertices. Those different notions of a minimal path enable us to understand how fast and how far information can spread through code review.

For more details on time-varying hypergraphs in general and modelling communication networks that emerges from code review with time-varying hypergraphs, have a look into [(Dorner et al. 2022)](https://dl.acm.org/doi/abs/10.1145/3544902.3546254).


## Installation

The simulation requires Python 3.10 and higher. Due to the [significant performance improvements in Python 3.11](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-faster-cpython) and the heavy CPU workload in the simulation, Python 3.11 is highly recommended! 

The project depends on two external libraries: [`tqdm`](https://github.com/tqdm/tqdm) and [`pandas`](https://pandas.pydata.org). Install via

```
python3 -m pip install -r requirements.txt
```

For a faster initial loading of the communication network, you **can optionally** install `orjson` via pip:

```
python3 -m pip install orjson
```

If `orjson` is not installed, built-in [`json`](https://docs.python.org/3/library/json.html) encoder is used.


## Usage

To run the full simulation, use

```
python3 -m simulation.run
```

Please notice that depending on your hardware, the complete simulation may run several days and max out the CPU power. On a Apple MacBook M1 Max, it takes about three full days to complete. The simulations is highly parallelized which means: The more cores, the better/faster. We also recommend at least 64 GB of RAM and at least 12 GB available storage for storing the results.

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
python -m unittest discover
```

The tests run also via [GitHub Actions](https://github.com/michaeldorner/information-diffusion-boundaries-in-code-review/actions). 

### Verification

To verify the [results](https://doi.org/10.5281/zenodo.7898863), compare the md5 hash values of our results (for example, via `md5 ./minimal_distances.*bz2` on macOS or `md5sum ./minimal_distances.*bz2` on Linux:

```
trivago.pickle.bz2 	 64c97c8ddb1e67cb70bfe297ad81c4ed
trivago.csv.bz2 	 a5e1a6d5230ac8c1888a711bd91f0420
spotify.pickle.bz2 	 c434b887fcf449dc7195cc428260b35c
spotify.csv.bz2 	 259532c46779df2702bcff0fa6c7932f
microsoft.pickle.bz2 	 f5b0beb747705fe3fcf4a84191bba937
microsoft.csv.bz2 	 08e93558473fb2b0a00de90e608901a3
```

We also provide a minimal unittest that compares the hashes from
set a command line variable `ZENODO_TOKEN=<...>` and run 

```
export ZENODO_TOKEN=<insert token here>
python3 -m unittest tests/test_results.py
```

Please notice: This simulation uses [Pickle Protocol version 5](https://peps.python.org/pep-0574/). Future protocol versions may produce different hashes if the internals change. `.csv` files, however, must produce always the same hashes.


## Visualization

Because of the large runtime of the simulation, we provide precomputed results of the simulation via [Zenodo](https://doi.org/10.5281/zenodo.7898863). You can download the results and place the `.pickle` and `.csv` files in the subfolder `data/minimal_paths`. Consider verify the `.pickle` and `.csv` files (see [Verification](#verification)).

To visualize the results and reproduce the tables and figures of the publication, see the Jupyter notebooks in the subfolder `notebooks/`.


## Credits

Thanks a lot

- [Andreas Bauer](https://github.com/andreas-bauer) for your valuable feedback in countless discussion.
- Students of the course _Software Testing_ in 2023 for their extraordinary efforts on developing a test suite for this project.


## License

Copyright © 2023 Michael Dorner

This work is licensed under [MIT license](LICENSE).
