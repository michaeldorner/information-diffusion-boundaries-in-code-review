import heapq
from enum import Enum
from datetime import datetime

from .model import TimeVaryingHypergraph


class DistanceType(Enum):
    SHORTEST = 0
    FASTEST = 1
    FOREMOST = 2


def single_source_dijkstra_hyperedges(hypergraph: TimeVaryingHypergraph, source_vertex, distance_type: DistanceType, min_timing=datetime.min):
    hedge_distances: dict = {}
    queue: list = []

    for source_hedge in hypergraph.hyperedges(source_vertex):
        match distance_type:
            case DistanceType.SHORTEST:
                init_value = 1
            case DistanceType.FASTEST:
                init_value = min_timing - min_timing
            case DistanceType.FOREMOST:
                init_value = hypergraph.timings(source_hedge)
        heapq.heappush(queue, (init_value, source_hedge))
        hedge_distances[source_hedge] = init_value

    while queue:
        prior_distance, source_hedge = heapq.heappop(queue)
        source_hedge_timing = hypergraph.timings(source_hedge)
        for vertex in hypergraph.vertices(source_hedge):
            for next_hedge in hypergraph.hyperedges(vertex):
                next_hedge_timing = hypergraph.timings(next_hedge)
                if source_hedge_timing < next_hedge_timing:
                    match distance_type:
                        case DistanceType.SHORTEST:
                            new_distance = prior_distance + 1
                        case DistanceType.FASTEST:
                            new_distance = prior_distance + (next_hedge_timing - source_hedge_timing)
                        case DistanceType.FOREMOST:
                            new_distance = next_hedge_timing
                    if next_hedge not in hedge_distances or new_distance < hedge_distances[next_hedge]:
                        hedge_distances[next_hedge] = new_distance
                        heapq.heappush(queue, (new_distance, next_hedge))

    vertex_distances: dict = {}
    for source_hedge, distance in hedge_distances.items():
        for vertex in hypergraph.vertices(source_hedge):
            if vertex not in vertex_distances or distance < vertex_distances[vertex]:
                vertex_distances[vertex] = distance
    vertex_distances.pop(source_vertex)
    return vertex_distances


def single_source_dijkstra_vertices(hypergraph: TimeVaryingHypergraph, source_vertex, distance_type: DistanceType, min_timing=datetime.min):
    distances: dict = {}
    queue: list = []

    source_hedge = None
    source_reachable = (source_vertex, source_hedge)

    match distance_type:
        case DistanceType.SHORTEST:
            init_distance = 0
        case DistanceType.FASTEST:
            init_distance = min_timing - min_timing
        case DistanceType.FOREMOST:
            init_distance = min_timing

    distances[source_reachable] = init_distance
    heapq.heappush(queue, (init_distance, source_reachable))

    while queue:
        distance, (vertex, source_hedge) = heapq.heappop(queue)
        for next_hedge in hypergraph.hyperedges(vertex):
            if source_hedge:
                source_hedge_timing = hypergraph.timings(source_hedge)
            else:  # damn source_hedge
                source_hedge_timing = hypergraph.timings(next_hedge)
            next_hedge_timing = hypergraph.timings(next_hedge)
            if not source_hedge or source_hedge_timing < next_hedge_timing:
                for next_vertex in hypergraph.vertices(next_hedge):
                    new_reachable = (next_vertex, next_hedge)
                    match distance_type:
                        case DistanceType.SHORTEST:
                            new_distance = distance + 1
                        case DistanceType.FASTEST:
                            new_distance = distance + (next_hedge_timing - source_hedge_timing)
                        case DistanceType.FOREMOST:
                            new_distance = next_hedge_timing
                    if new_reachable not in distances or new_distance < distances[new_reachable]:
                        distances[new_reachable] = new_distance
                        heapq.heappush(queue, (new_distance, new_reachable))
    minimal_distances: dict = {}
    for (vertex, _), distance in distances.items():
        if vertex not in minimal_distances or distance < minimal_distances[vertex]:
            minimal_distances[vertex] = distance
    minimal_distances.pop(source_vertex)

    return minimal_distances
