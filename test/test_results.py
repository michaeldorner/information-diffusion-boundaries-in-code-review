import unittest
import hashlib
import os
from pathlib import Path

try:
    import requests
    REQUESTS_INSTALLED = True
except ModuleNotFoundError:
    REQUESTS_INSTALLED = False

ZENODO_ACCESS_TOKEN = os.environ.get('ZENODO_ACCESS_TOKEN')


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):  # spare some memory
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class ResultsTest(unittest.TestCase):
    @unittest.skipIf(not ZENODO_ACCESS_TOKEN or not REQUESTS_INSTALLED, 'Skipped because no Zenodo access token was provided.')
    def test_results(self):
        zenodo_access_token = os.environ.get('ZENODO_ACCESS_TOKEN')
        response = requests.get('https://zenodo.org/api/records/8042256',
                                params={'access_token': zenodo_access_token}, timeout=10)
        response.raise_for_status()
        zenodo_reference = {record['key']: record['checksum'][len(
            'md5:'):] for record in response.json()['files']}
        if zenodo_reference:
            for file_path in sorted(Path('./').glob('./data/minimal_distances/*.bz2'), reverse=True):
                file_name = file_path.name
                with self.subTest(file_name=file_name):
                    md5_hash = md5(file_path)
                    md5_hash_reference = zenodo_reference.get(file_name)
                    self.assertEqual(
                        md5_hash, md5_hash_reference, 'md5 hash is not equivalent with reference on Zenodo')
