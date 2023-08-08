import unittest
from pathlib import Path

from simulation.run import AVAILABLE_DATA_SETS


class TestData(unittest.TestCase):
    def test_data(self):
        for data_set in AVAILABLE_DATA_SETS:
            with self.subTest(data_set=data_set):
                path = Path(f'./data/networks/{data_set}.json.bz2')
                self.assertTrue(path.exists(), f'{path} does not exist')
