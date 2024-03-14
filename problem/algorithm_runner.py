import glob
import os
from tqdm import tqdm


def run_algorithm_on_dataset(algorithm, dataset_folder, output_folder):
    input_files = sorted(glob.glob(f"{dataset_folder}/*.txt"))
    for input_file in tqdm(input_files):
        output_file = f"{output_folder}/{os.path.basename(input_file).replace('input', 'output')}"
        output_file = output_file.replace('.txt', '.json')
        try:
            algorithm(input_file, output_file)
        except Exception as e:
            print(f"An error occurred while running the algorithm on {input_file}: {e}")
            continue
