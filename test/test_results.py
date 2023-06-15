import unittest
import hashlib
import os
from pathlib import Path

import requests


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):  # spare some memory
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class ResultsTest(unittest.TestCase):
    def setUp(self) -> None:
        zenodo_access_token = os.environ.get('ZENODO_ACCESS_TOKEN')
        if zenodo_access_token:
            response = requests.get('https://zenodo.org/api/records/8042256', params={'access_token': zenodo_access_token}, timeout=10)
            response.raise_for_status()
            self.zenodo_reference = {record['key']: record['checksum'][len('md5:'):] for record in response.json()['files']}
        else:
            self.zenodo_reference = None
            print('skip')

        return super().setUp()

    @unittest.skipIf(os.environ.get('ZENODO_ACCESS_TOKEN') is None, 'Skipped because no Zenodo access token was provided.')
    def test_results(self):
        if self.zenodo_reference:
            for file_path in sorted(Path('./').glob('./data/minimal_distances/*.bz2'), reverse=True):
                file_name = file_path.name
                with self.subTest(file_name=file_name):
                    md5_hash = md5(file_path)
                    md5_hash_reference = self.zenodo_reference.get(file_name)
                    self.assertEqual(md5_hash, md5_hash_reference, 'md5 hash is not equivalent with reference on Zenodo')
