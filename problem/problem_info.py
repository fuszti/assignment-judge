from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
import networkx as nx


class TaskStatus(Enum):
    PENDING = 0
    PICKED = 1
    DROPPED = 2

@dataclass
class TaskInfo:
    release_time: int
    start_node: int
    end_node: int
    status: TaskStatus = TaskStatus.PENDING

    def is_available(self, current_time):
        return self.release_time <= current_time and self.status == TaskStatus.PENDING
    
    def is_released(self, current_time):
        return self.release_time <= current_time
    

@dataclass
class ProblemInfo:
    graph: nx.Graph
    vehicles_positions: List[Tuple[int]]
    """ (a, b) means that the vehicle on edge a-b, (a, a) means that the vehicle is on node a"""
    tasks_info: List[TaskInfo]

def read_problem_info(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Extract the first line information
    nodes, edges, tasks, vehicles = map(int, lines[0].split())

    # Initialize the graph as a networkx graph
    graph = nx.Graph()

    # Parse the vehicle starting positions
    vehicles_positions = list(map(lambda node_str: (int(node_str), int(node_str)), lines[1].split()))

    # Parse the edges and keep only the shortest edge between two nodes
    for i in range(2, 2 + edges):
        from_node, to_node, length = map(int, lines[i].split())
        if graph.has_edge(from_node, to_node):
            if graph[from_node][to_node]['weight'] > length:
                graph[from_node][to_node]['weight'] = length
        else:
            graph.add_edge(from_node, to_node, weight=length)

    # Parse the tasks
    tasks_info = []
    for i in range(2 + edges, 2 + edges + tasks):
        release_time, start_node, end_node = map(int, lines[i].split())
        tasks_info.append(TaskInfo(release_time, start_node, end_node))
    return ProblemInfo(graph, vehicles_positions, tasks_info)