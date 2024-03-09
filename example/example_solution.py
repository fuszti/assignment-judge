import argparse
import json
import networkx as nx

# argparse the input file txt and output file json
parser = argparse.ArgumentParser(description='Parse the input file and output the commands')
parser.add_argument('input', type=str, help='The input file')
parser.add_argument('output', type=str, help='The output file')
args = parser.parse_args()

# Read the input file
with open(args.input, 'r') as file:
    lines = file.readlines()

# Extract the first line information
nodes, edges, tasks, vehicles = map(int, lines[0].split())

# Initialize the graph as a networkx graph
graph = nx.Graph()

# Parse the vehicle starting positions
vehicles_positions = list(map(int, lines[1].split()))
vehicles_info = [{'position': pos, 'task': None} for pos in vehicles_positions]

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
    tasks_info.append({'release_time': release_time, 'start_node': start_node, 'end_node': end_node, 'picked': False})

# Initialize the simulation
simulation_steps = []
current_time = 0
vehicle = vehicles_info[0]  # We only move the first vehicle

# Simulation loop
while tasks_info:
    commands = {}

    if 'edge' in vehicle:
        # If the vehicle is on an edge, move it forward
        current_edge = vehicle['edge']
        time_elapsed = current_time - vehicle['started_edge']
        if time_elapsed >= current_edge[2]:
            vehicle['position'] = current_edge[1]
            vehicle.pop('edge', None)  # Remove edge if exists
            vehicle.pop('started_edge', None) 
        else:
            commands["1"] = "FORWARD"
    if 'edge' not in vehicle:
        # If the vehicle has a task and is on a node, move towards the end node
        if vehicle['task']:
            if vehicle['position'] == vehicle['task']['end_node']:
                vehicle['task'] = None
                commands["1"] = "DROP"
            else:
                # Find the next node to move to on the shortest path to the task's end node
                path = nx.shortest_path(graph, vehicle['position'], vehicle['task']['end_node'], weight='weight')
                next_node = path[1]
                edge_length = graph[vehicle['position']][next_node]['weight']
                vehicle['edge'] = (vehicle['position'], next_node, edge_length)  # Vehicle is now on an edge
                vehicle['started_edge'] = current_time
                commands["1"] = f"GO {vehicle['position']} {next_node}"
        else:
            first_available_task = next((task for task in tasks_info if task['release_time'] <= current_time and not task['picked']), None)
            if first_available_task:
                if vehicle["position"] == first_available_task["start_node"]:
                    vehicle["task"] = first_available_task
                    first_available_task["picked"] = True
                    commands["1"] = "PICK UP"
                else:
                    path = nx.shortest_path(graph, vehicle['position'], first_available_task['start_node'], weight='weight')
                    next_node = path[1]
                    edge_length = graph[vehicle['position']][next_node]['weight']
                    vehicle['edge'] = (vehicle['position'], next_node, edge_length)
                    vehicle['started_edge'] = current_time
                    commands["1"] = f"GO {vehicle['position']} {next_node}"
            else:
                commands["1"] = "IDLE"
    #####


    # Add the commands for the current step
    for other_vehicle_idx in range(1, vehicles):
        commands[str(other_vehicle_idx + 1)] = "IDLE"
    simulation_steps.append(commands)
    current_time += 1

    # Remove completed tasks
    tasks_info = [task for task in tasks_info if not task['picked'] or vehicle['position'] != task['end_node']]

# Output the commands
output = {"commands": simulation_steps}

# Write the output to the output file json
# Convert the Python dictionary to a pretty-printed JSON string
formatted_json = json.dumps(output, indent=4)
with open(args.output, 'w') as file:
    file.write(formatted_json)

