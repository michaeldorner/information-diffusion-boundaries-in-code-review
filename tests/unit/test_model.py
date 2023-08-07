import unittest

from simulation.model import CommunicationNetwork, TimeVaryingHypergraph, EntityNotFound


class TimeVaryingHypergraphTest(unittest.TestCase):
    timings = {'h1': 1, 'h2': 2, 'h3': 3}
    hyperedges = {'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}
    hypergraph = TimeVaryingHypergraph(hyperedges, timings)

    def test_vertices(self):
        for hedge, vertices in TimeVaryingHypergraphTest.hyperedges.items():
            with self.subTest(hyperedge=hedge):
                self.assertEqual(TimeVaryingHypergraphTest.hypergraph.vertices(hedge), set(vertices))

    def test_hyperedges(self):
        self.assertEqual(TimeVaryingHypergraphTest.hypergraph.hyperedges('v1'), {'h1'})

    def test_timings(self):
        self.assertEqual(TimeVaryingHypergraphTest.hypergraph.timings(), TimeVaryingHypergraphTest.timings)

    def test_unknown_vertex(self):
        self.assertRaises(EntityNotFound, TimeVaryingHypergraphTest.hypergraph.vertices, 'vx')

    def test_unknown_hyperedge(self):
        self.assertRaises(EntityNotFound, TimeVaryingHypergraphTest.hypergraph.hyperedges, 'hx')


class CommunicationNetworkTest(unittest.TestCase):
    timings = {'h1': 1, 'h2': 2, 'h3': 3}
    hyperedges = {'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}
    communication_network = CommunicationNetwork(hyperedges, timings)

    def test_pairwise_vertex_participant_equivalence(self):
        for hedge in list(CommunicationNetworkTest.hyperedges):
            with self.subTest(hyperedge=hedge):
                self.assertEqual(CommunicationNetworkTest.communication_network.vertices(hedge), CommunicationNetworkTest.communication_network.participants(hedge))

    def test_vertex_participant_equivalence(self):
        self.assertEqual(CommunicationNetworkTest.communication_network.vertices(), CommunicationNetworkTest.communication_network.participants())

    def test_pairwise_hyperedge_channel_equivalence(self):
        for vertex in {v for vertices in CommunicationNetworkTest.hyperedges.values() for v in vertices}:
            with self.subTest(hyperedge=vertex):
                self.assertEqual(CommunicationNetworkTest.communication_network.hyperedges(vertex), CommunicationNetworkTest.communication_network.channels(vertex))

    def test_hyperedge_channel_equivalence(self):
        self.assertEqual(CommunicationNetworkTest.communication_network.hyperedges(), CommunicationNetworkTest.communication_network.channels())


class ParametrizedCommunicationNetworkTest(unittest.TestCase):
    def test_with_paramtrization(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        with self.subTest():
            self.assertEqual(len(communciation_network.participants()), 37103)
        with self.subTest():
            self.assertEqual(len(communciation_network.channels()), 309740)
