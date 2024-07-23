import os
import random
import shutil

def sample_subdirectories(root_dirs, sample_size_per_dir, output_dir):
    """
    Takes a sample of subdirectories from specific directories and saves them into corresponding directories.

    Parameters:
        root_dirs (list): List of root directories from which to sample subdirectories.
        sample_size_per_dir (int): The number of subdirectories to sample from each directory.
        output_dir (str): The directory to save the sampled subdirectories.

    Returns:
        None
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    common_parent_dir = os.path.basename(os.path.dirname(os.path.commonpath(root_dirs)))

    for root_dir in root_dirs:
        # List all subdirectories in the root directory
        all_subdirectories = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

        # Check if sample size is greater than total number of subdirectories
        if sample_size_per_dir > len(all_subdirectories):
            print(f"Sample size for {root_dir} exceeds the total number of subdirectories.")
            continue

        # Randomly select sample_size_per_dir subdirectories
        sampled_subdirectories = random.sample(all_subdirectories, sample_size_per_dir)

        # Create a directory for the parent directory if it doesn't exist
        parent_output_dir = os.path.join(output_dir, common_parent_dir)
        if not os.path.exists(parent_output_dir):
            os.makedirs(parent_output_dir)

        # Copy sampled subdirectories to the output directory
        for subdirectory in sampled_subdirectories:
            output_subdirectory = os.path.join(parent_output_dir, os.path.basename(subdirectory))
            if os.path.exists(output_subdirectory):
                output_subdirectory += "_copy"  # Add "_copy" suffix if directory already exists
            shutil.copytree(subdirectory, output_subdirectory)

        print(f"Sampled {sample_size_per_dir} subdirectories from {root_dir} to {parent_output_dir}")

root_directories = [r"FairMOT_ROOT\src\lib\datasets\dataset\fish\images\train", r"FairMOT_ROOT\src\lib\datasets\dataset\fish\labels_with_ids\train"]
output_directory = r"FairMOT_ROOT\src\lib\datasets\dataset\sanity"
sample_size_per_directory = 10

sample_subdirectories(root_directories, sample_size_per_directory, output_directory)
