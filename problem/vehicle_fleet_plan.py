from enum import Enum
from typing import Dict, List

class Command(Enum):
    FORWARD = 'FORWARD'
    PICKUP = 'PICK UP'
    DROP = 'DROP'
    GO = 'GO'
    IDLE = 'IDLE'

    @staticmethod
    def from_str(command_str: str):
        if command_str[:2] == 'GO':
            return Command.GO
        return Command(command_str)
    
    @staticmethod
    def get_args_from_str(command_str: str):
        if command_str[:2] == 'GO':
            return tuple(map(int, command_str.split()[1:]))
        return ()


class VehicleFleetPlan:
    def __init__(self, plan: List[Dict[str, str]]):
        self.plan = plan
    
    def __getitem__(self, key):
        command_dict = {}
        for vehicle_id, command_str in self.plan[key].items():
            vehicle_id_int = int(vehicle_id) - 1
            command_dict[vehicle_id_int] = (Command.from_str(command_str), 
                                            Command.get_args_from_str(command_str))
        return command_dict

    def __len__(self):
        return len(self.plan)