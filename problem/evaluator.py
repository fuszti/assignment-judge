import argparse
import json

from problem.problem_info import read_problem_info
from problem.simulator import ProblemState, Simulator
from problem.vehicle_fleet_plan import VehicleFleetPlan



def evaluate(input_path, output_json):
    problem_info = read_problem_info(input_path)
    fleet_plan = VehicleFleetPlan(output_json["commands"])
    init_problem_state = ProblemState(problem_info)
    simulator = Simulator(problem_state=init_problem_state)
    for command_dict in fleet_plan:
        simulator.apply(command_dict)
    return simulator.get_score()


if __name__ == "__main__":
    # argparse the input text file and the output json file and call evaluate
    parser = argparse.ArgumentParser(description='Evaluate the output json file')
    parser.add_argument('input', type=str, help='The input text file')
    parser.add_argument('output', type=str, help='The output json file')
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    # Read the output json file
    with open(output_path, 'r') as file:
        output_json = json.load(file)

    # Evaluate the output json file
    score = evaluate(input_path, output_json)

    # Print the score
    print(f"The score is: {score}")