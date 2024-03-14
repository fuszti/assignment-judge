import argparse
import glob
import json
import os
from tqdm import tqdm

from problem.problem_info import read_problem_info
from problem.simulator import ProblemState, Simulator
from problem.vehicle_fleet_plan import VehicleFleetPlan

def evaluate_dataset(input_folder, output_folder):
    input_files = sorted(glob.glob(f"{input_folder}/*.txt"))
    full_score = 0.0
    for input_file in tqdm(input_files, desc="Evaluating"):
        output_file = f"{output_folder}/{os.path.basename(input_file).replace('input', 'output')}"
        output_file = output_file.replace('.txt', '.json')
        with open(output_file, 'r') as file:
            output_json = json.load(file)
        try:
            full_score += evaluate(input_file, output_json)
        except Exception as e:
            print(f"An error occurred while evaluating the output file {output_file}: {e}")
    return full_score


def evaluate(input_path, output_json):
    problem_info = read_problem_info(input_path)
    fleet_plan = VehicleFleetPlan(output_json["commands"])
    init_problem_state = ProblemState(problem_info)
    simulator = Simulator(problem_state=init_problem_state)
    for command_dict in fleet_plan:
        simulator.apply(command_dict)
    return simulator.get_score()
