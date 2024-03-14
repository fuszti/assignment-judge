import glob
import os
from tqdm import tqdm


def run_algorithm_on_dataset(algorithm, dataset_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for f in glob.glob(f"{output_folder}/*"):
        os.remove(f)
    input_files = sorted(glob.glob(f"{dataset_folder}/*.txt"))
    for input_file in tqdm(input_files, desc="Running your algorithm on the dataset"):
        output_file = f"{output_folder}/{os.path.basename(input_file).replace('input', 'output')}"
        output_file = output_file.replace('.txt', '.json')
        try:
            algorithm(input_file, output_file)
        except Exception as e:
            print(f"An error occurred while running the algorithm on {input_file}: {e}")
            continue
