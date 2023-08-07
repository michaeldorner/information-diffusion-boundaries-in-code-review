import unittest
from pathlib import Path

from simulation.run import run_simulation, AVAILABLE_DATA_SETS


class RunTest(unittest.TestCase):
    def test_run_simulation(self):
        for data_set in AVAILABLE_DATA_SETS:
            with self.subTest(data_set=data_set):
                self.assertTrue(Path(f'../data/networks/{data_set}.json.bz2').exists(), f'{data_set} does not exist')
