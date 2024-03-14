import argparse
import networkx as nx
import random
from tqdm import tqdm

from problem.predefined_graph_generators import collection_small, collection_public
from problem.problem_info import TaskInfo

MAX_VEHICLE_COUNT = 30
MAX_TASK_COUNT = 150
MAX_WEIGHT = 25

def main():
    parser = argparse.ArgumentParser(description='Generate the input text files')
    parser.add_argument('--output_folder', type=str, help='The output folder')
    args = parser.parse_args()
    output_folder = args.output_folder
    generate_problems(output_folder, collection_public)

def generate_problems(output_folder, random_graphs):
    for i, graph in tqdm(enumerate(random_graphs)):
        g = graph()
        generate_problem(output_folder, 
                         idx=i, 
                         graph=g)

def generate_problem(output_folder, idx, graph):
    graph = make_connected(graph)
    graph = generate_random_weights(graph)
    vehicles_positions = generate_random_vehicles_positions(graph)
    tasks_info = generate_random_tasks_info(graph)
    input_file_path = f"{output_folder}/input_{idx}.txt"
    with open(input_file_path, 'w') as file:
        file.write(f"{len(graph.nodes)} {len(graph.edges)} {len(tasks_info)} {len(vehicles_positions)}\n")
        file.write(f"{' '.join(map(str, vehicles_positions))}\n")
        for u, v in graph.edges:
            file.write(f"{u} {v} {graph[u][v]['weight']}\n")
        for task_info in tasks_info:
            file.write(f"{task_info.release_time} {task_info.start_node} {task_info.end_node}\n")


def make_connected(graph):
    if not nx.is_connected(graph):
        components = list(nx.connected_components(graph))
        for i in range(1, len(components)):
            u = random.choice(list(components[0]))
            v = random.choice(list(components[i]))
            graph.add_edge(u, v, weight=random.randint(1, 150))
    return graph

def generate_random_weights(graph):
    max_weight = random.randint(1, MAX_WEIGHT)
    for u, v in graph.edges:
        graph[u][v]['weight'] = random.randint(1, max_weight)
    return graph

def generate_random_vehicles_positions(graph):
    vehicles_positions = []
    upper_limit = min(len(graph.nodes) // 2, MAX_VEHICLE_COUNT)
    number_of_vehicle_positions = random.randint(5, upper_limit)
    for _ in range(number_of_vehicle_positions):
        node = random.choice(list(graph.nodes))
        vehicles_positions.append(node)
    return vehicles_positions

def generate_random_tasks_info(graph):
    tasks_info = []
    upper_limit = min(len(graph.nodes) // 2, MAX_TASK_COUNT)
    number_of_tasks = random.randint(5, upper_limit)
    # starting node are different for each task
    random_order_of_nodes = list(graph.nodes)
    random.shuffle(random_order_of_nodes)
    for i in range(number_of_tasks):
        release_time = random.randint(1, 100)
        start_node = random_order_of_nodes[i]
        end_node = random.choice(list(graph.nodes))
        while end_node == start_node:
            end_node = random.choice(list(graph.nodes))
        tasks_info.append(TaskInfo(release_time, start_node, end_node))
    tasks_info.sort(key=lambda task_info: task_info.release_time)
    return tasks_info

if __name__ == "__main__":
    main()
    