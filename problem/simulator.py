from copy import deepcopy
from typing import Dict, Tuple
from problem.problem_info import ProblemInfo, TaskStatus
from problem.vehicle_fleet_plan import Command, VehicleFleetPlan


class ProblemState:
    def __init__(self, problem_info: ProblemInfo):
        self._graph = problem_info.graph
        self._vehicles_positions = problem_info.vehicles_positions
        self._tasks_info = problem_info.tasks_info
        self._current_time = 0
        self._vehicles_went_on_edge = {}
        self._vehicles_pickup_tasks = {}
    
    def __deepcopy__(self, memo):
        # Create a new instance without calling __init__
        new_instance = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_instance
        for k, v in self.__dict__.items():
            if k == "_graph":  # Don't deepcopy _graph
                setattr(new_instance, k, v)
            else:
                setattr(new_instance, k, deepcopy(v, memo))
        return new_instance

    @property
    def problem_info(self):
        return ProblemInfo(self._graph, self._vehicles_positions, self._tasks_info)
    
    @property
    def current_time(self):
        return self._current_time
    
    def step(self, commands: Dict[str, Tuple[Command, Tuple[int]]]):
        new_state = deepcopy(self)
        for vehicle_id, (command, args) in commands.items():
            if command == Command.FORWARD:
                if vehicle_id in self._vehicles_went_on_edge:
                    edge_started_time = self._vehicles_went_on_edge[vehicle_id]
                    time_elapsed = self._current_time - edge_started_time + 1
                    from_node, to_node = self._vehicles_positions[vehicle_id]
                    edge_length = self._graph[from_node][to_node]['weight']
                    if time_elapsed >= edge_length:
                        new_state._vehicles_positions[vehicle_id] = (to_node, to_node)
                        new_state._vehicles_went_on_edge.pop(vehicle_id)
                else:
                    raise ValueError(f"Vehicle {vehicle_id} is not on an edge")
            elif command == Command.PICKUP:
                picked_task_idx = [idx for idx, t in enumerate(self._tasks_info) if t.start_node == self._vehicles_positions[vehicle_id][0]]
                if vehicle_id in self._vehicles_pickup_tasks:
                    raise ValueError(f"Vehicle {vehicle_id} already picked up a task")
                if picked_task_idx:
                    new_state._vehicles_pickup_tasks[vehicle_id] = picked_task_idx[0]
                    new_state._tasks_info[picked_task_idx[0]].status = TaskStatus.PICKED
                else:
                    raise ValueError(f"Vehicle {vehicle_id} has no task to pick up")
            elif command == Command.DROP:
                if vehicle_id not in self._vehicles_pickup_tasks:
                    raise ValueError(f"Vehicle {vehicle_id} has not picked up a task")
                picked_task_idx = self._vehicles_pickup_tasks[vehicle_id]
                if self._tasks_info[picked_task_idx].end_node == self._vehicles_positions[vehicle_id][0]:
                    new_state._tasks_info[picked_task_idx].status = TaskStatus.DROPPED
                    del new_state._vehicles_pickup_tasks[vehicle_id]
                else:
                    raise ValueError(f"Vehicle {vehicle_id} is not on the end node of its task")
            elif command == Command.GO:
                from_node, to_node = args
                if self._vehicles_positions[vehicle_id][1] != from_node:
                    raise ValueError(f"Vehicle {vehicle_id} is not on node {from_node}")
                if from_node != self._vehicles_positions[vehicle_id][0]:
                    raise ValueError(f"Vehicle {vehicle_id} is not on node {from_node}")
                if to_node not in self._graph[from_node]:
                    raise ValueError(f"Node {to_node} is not reachable from node {from_node}")
                edge_length = self._graph[from_node][to_node]['weight']
                if edge_length > 1:
                    new_state._vehicles_positions[vehicle_id] = (from_node, to_node)
                    new_state._vehicles_went_on_edge[vehicle_id] = self._current_time
                else:
                    new_state._vehicles_positions[vehicle_id] = (to_node, to_node)
            elif command == Command.IDLE:
                pass
            else:
                raise ValueError(f"Unknown command {command}")
        new_state._current_time += 1
        return new_state
    
    def is_terminated(self):
        for task_info in self._tasks_info:
            if task_info.status != TaskStatus.DROPPED:
                return False
        return True

class Simulator:
    def __init__(self, problem_state: ProblemState):
        self.problem_state = problem_state
        self.invalid_command_happened = False
        self.score = -1
    
    def apply(self, commands: Dict[str, Tuple[Command, Tuple[int]]]) -> None:
        try:
            self.problem_state = self.problem_state.step(commands)
            if self.score == -1 and self.problem_state.is_terminated():
                self.score = self.problem_state.current_time
        except ValueError as e:
            self.invalid_command_happened = True
    
    def is_terminated(self) -> bool:
        return self.problem_state.is_terminated()
    
    def is_invalid(self) -> bool:
        return self.invalid_command_happened
    
    def get_score(self) -> float:
        if self.invalid_command_happened:
            return float('inf')
        if self.score == -1:
            return float('inf')
        return float(self.score)
        