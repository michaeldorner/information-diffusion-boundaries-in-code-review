import unittest
from unittest.mock import patch
import argparse
import multiprocessing as mp

from simulation.run import run_simulation


class RunTest(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(select=['trivago'], num_processes=mp.cpu_count(), hyperedge_dijkstra=True, vertex_dijkstra=False))
    def test_run_simulation_with_hyperedge_dijkstra(self, _):
        self.assertIsNone(run_simulation(), 'Larger problem')

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(select=['trivago'], num_processes=mp.cpu_count(), hyperedge_dijkstra=False, vertex_dijkstra=True))
    def test_run_simulation_with_vertex_dijkstra(self, _):
        self.assertIsNone(run_simulation(), 'Larger problem')
