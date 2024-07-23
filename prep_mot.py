import os
import pandas as pd

def clean_and_save(input_file, output_directory):
    # Read the TXT file with the first 6 columns and specified column names
    df = pd.read_csv(input_file, usecols=[0, 1, 2, 3, 4, 5], names=['frame', 'id', 'x', 'y', 'x_offset', 'y_offset'])

    # Define the output file path in the output directory with the same file name
    output_file = os.path.join(output_directory, os.path.basename(input_file))

    # Save the cleaned DataFrame back to the output file without an index
    df.to_csv(output_file, sep=',', index=False, header=True)

def clean_all_txt_files(input_directory, output_directory):
    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_directory, filename)
            print(f"Cleaning file: {input_file}")

            # Clean and save the TXT file to the output directory
            clean_and_save(input_file, output_directory)

if __name__ == "__main__":
    # Specify the input and output directories
    input_directory = 'mots/mots'
    output_directory = 'mot_clean'

    # Clean all TXT files in the input directory and save them to the output directory
    clean_all_txt_files(input_directory, output_directory)

