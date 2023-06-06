import unittest

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPathTest(unittest.TestCase):
    communication_network_1 = CommunicationNetwork({
        'h1': ['v1', 'v2'],
        'h2': ['v2', 'v3'],
        'h3': ['v3', 'v4']
    }, {
        'h1': 1,
        'h2': 2,
        'h3': 3
    }, name='1')

    minimal_paths_1 = {
        'v1': {
            DistanceType.SHORTEST: {'v2': 1, 'v3': 2, 'v4': 3},
            DistanceType.FASTEST: {'v2': 0, 'v3': 1, 'v4': 2},
            DistanceType.FOREMOST: {'v2': 1, 'v3': 2, 'v4': 3},
        }
    }

    communication_network_2 = CommunicationNetwork({
        'h0': ['v0', 'v1'],
        'h1': ['v1', 'v9'],
        'h2': ['v2', 'v6'],
        'h3': ['v3', 'v8'],
        'h4': ['v4', 'v3'],
        'h5': ['v5', 'v6'],
        'h6': ['v6', 'v7'],
        'h7': ['v7', 'v0'],
        'h9': ['v9', 'v8'],
        'h10': ['v10', 'v8'],
    }, {
        'h0': 176,
        'h1': 68,
        'h2': 187,
        'h3': 163,
        'h4': 57,
        'h5': 160,
        'h6': 111,
        'h7': 174,
        'h8': 82,
        'h9': 49,
        'h10': 7,
    }, name='2')

    minimal_paths_2 = {
        'v4': {
            DistanceType.SHORTEST: {'v3': 1, 'v8': 2},
            DistanceType.FASTEST: {'v3': 0, 'v8': 106},
            DistanceType.FOREMOST: {'v3': 57, 'v8': 163},
        }
    }

    def test_single_source_dijkstra_vertices(self):
        for communication_network, minimal_paths in ((MinimalPathTest.communication_network_1, MinimalPathTest.minimal_paths_1), (MinimalPathTest.communication_network_2, MinimalPathTest.minimal_paths_2)):
            for start_vertex, _minimal_paths in minimal_paths.items():
                for distance_type in DistanceType:
                    with self.subTest(distance_type=distance_type.name, communication_network=communication_network.name):
                        self.assertEqual(single_source_dijkstra_vertices(communication_network, start_vertex, distance_type, min_timing=0), _minimal_paths[distance_type])

    def test_single_source_dijkstra_hyperedges(self,):
        for communication_network, minimal_paths in ((MinimalPathTest.communication_network_1, MinimalPathTest.minimal_paths_1), (MinimalPathTest.communication_network_2, MinimalPathTest.minimal_paths_2)):
            for start_vertex, _minimal_paths in minimal_paths.items():
                for distance_type in DistanceType:
                    with self.subTest(distance_type=distance_type.name, communication_network=communication_network.name):
                        self.assertEqual(single_source_dijkstra_hyperedges(communication_network, start_vertex, distance_type, min_timing=0), _minimal_paths[distance_type])

    def test_pairwise_minimal_distance(self):
        for communication_network in (MinimalPathTest.communication_network_1, MinimalPathTest.communication_network_2, ):
            for distance_type in DistanceType:
                for vertex in communication_network.vertices():
                    with self.subTest(distance_type=distance_type.name, vertex=vertex):
                        result_1 = single_source_dijkstra_vertices(communication_network, vertex, distance_type, min_timing=0)
                        result_2 = single_source_dijkstra_hyperedges(communication_network, vertex, distance_type, min_timing=0)
                        self.assertEqual(result_1, result_2, f'Single-source Dijkstra implementations for {distance_type.name} and vertex {vertex} are not equivalent')
