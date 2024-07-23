import os

# Directory containing the JPEG files to be renamed
directory = 'FairMOT_ROOT/src/data/fish/images/train'

# Get a list of all JPEG files in the directory
jpeg_files = [file for file in os.listdir(directory) if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg')]

# Sort files alphabetically
jpeg_files.sort()

# Counter for renaming
counter = 1

# Loop through each file and rename
for file in jpeg_files:
    # Generate the new file name
    new_filename = '{:05d}.jpeg'.format(counter)
    
    # Construct the full paths
    old_path = os.path.join(directory, file)
    new_path = os.path.join(directory, new_filename)
    
    # Rename the file
    os.rename(old_path, new_path)
    
    # Increment the counter
    counter += 1
