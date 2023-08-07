import argparse
from pathlib import Path
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
from tqdm import tqdm

from .model import CommunicationNetwork
from .minimal_distances import single_source_dijkstra_hyperedges, single_source_dijkstra_vertices, DistanceType

AVAILABLE_DATA_SETS = ('microsoft', 'spotify', 'trivago')


def run_simulation():
    parser = argparse.ArgumentParser(description='Simulating information diffusion in code review communication networks')
    parser.add_argument('--select', type=str, nargs='+', choices=AVAILABLE_DATA_SETS, help='Load a subset of the available data', default=AVAILABLE_DATA_SETS)
    parser.add_argument('--num_processes', type=int, default=mp.cpu_count(), help='Number of parallel processes (default # of CPUs)')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--hyperedge_dijkstra', action='store_false', help='Use single-source Dikstra algorithm via hyperedges; tend to be faster than --vertex_dijkstra (default)')
    group.add_argument('--vertex_dijkstra', action='store_true', help='Use single-source Dikstra algorithm via vertices')

    args = parser.parse_args()

    result_dir_path = Path('./data/minimal_distances/')
    result_dir_path.mkdir(parents=True, exist_ok=True)

    if args.hyperedge_dijkstra:
        single_source_dijkstra = single_source_dijkstra_hyperedges
    else:
        single_source_dijkstra = single_source_dijkstra_vertices

    for name in args.select:
        communication_network = CommunicationNetwork.from_json(f'./data/networks/{name}.json.bz2', name=name)

        participants = tuple(sorted(communication_network.participants()))
        category = pd.api.types.CategoricalDtype(categories=participants, ordered=False)
        data_frames = []
        for distance_type in DistanceType:
            distance_type_name = distance_type.name.lower()
            min_distances = []
            with ProcessPoolExecutor(mp_context=mp.get_context('spawn'), max_workers=9) as executor:
                futures = {executor.submit(
                    single_source_dijkstra, communication_network, p, distance_type): p for p in participants}
                for future in tqdm(as_completed(futures), total=len(futures), desc=f'Find all {distance_type_name} distances at {name.capitalize()}'.ljust(36)):
                    source = futures[future]
                    if future.exception():
                        raise future.exception()
                    for target, distance in future.result().items():
                        min_distances += [(source, target, distance)]
            min_distances_df = pd.DataFrame(
                min_distances, columns=['source', 'target', 'distance'])
            min_distances = None
            min_distances_df.source = min_distances_df.source.astype(
                category)
            min_distances_df.target = min_distances_df.target.astype(
                category)
            data_frames += [min_distances_df.set_index(['source', 'target']).distance.rename(distance_type_name).sort_index()]
        result = pd.concat(data_frames, axis=1).sort_index()
        result.info(verbose=True, memory_usage=True, show_counts=True)
        result.to_csv(result_dir_path/f'{name}.csv.bz2', compression='bz2')
        result.to_pickle(result_dir_path/f'{name}.pickle.bz2', compression='bz2')


if __name__ == '__main__':
    run_simulation()
