import os

# File path definitions
input_file_path = 'mots/mots/236_1.txt'
output_directory = 'gt_mot'

# Function to generate the output file name based on the input file name
def get_output_file_path(input_path, output_dir):
    filename = os.path.basename(input_path)
    base_name, extension = os.path.splitext(filename)
    new_filename = f'{base_name}_gt{extension}'
    return os.path.join(output_dir, new_filename)

# Function to process the input file and generate the output file
def process_file(input_path, output_dir):
    output_path = get_output_file_path(input_path, output_dir)
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    # Read the input file and store lines in a list
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
    
    # Process each line and split by commas
    processed_lines = [line.strip().split(',') for line in lines]
    
    # Sort the lines based on the first column, treating it as a number
    processed_lines.sort(key=lambda x: int(x[0]))
    
    # Modify the last four columns
    for values in processed_lines:
        values[-4:] = [1, -1, -1, -1]
    
    # Write the sorted and modified lines to the output file
    with open(output_path, 'w') as outfile:
        for values in processed_lines:
            modified_line = ','.join(map(str, values))
            outfile.write(modified_line + '\n')

# Call the function to process the file
process_file(input_file_path, output_directory)