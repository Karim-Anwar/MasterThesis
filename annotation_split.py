import os
import shutil

# Define the directories
train_mp4_directory = 'vids/train'
val_mp4_directory = 'vids/val'
txt_directory = 'mot_clean'
train_destination_directory = 'mot_clean/train'
val_destination_directory = 'mot_clean/val'

# Get a list of mp4 files in train directory
train_mp4_files = os.listdir(train_mp4_directory)
train_mp4_file_names = [os.path.splitext(file)[0] for file in train_mp4_files]

# Get a list of mp4 files in val directory
val_mp4_files = os.listdir(val_mp4_directory)
val_mp4_file_names = [os.path.splitext(file)[0] for file in val_mp4_files]

# List to store mp4 files without corresponding txt files
unmatched_mp4_files = []

# Iterate through txt files
for txt_file in os.listdir(txt_directory):
    # Check if the txt file name matches any mp4 file name in train directory
    if os.path.splitext(txt_file)[0] in train_mp4_file_names:
        # Move the txt file to the train destination directory
        shutil.move(os.path.join(txt_directory, txt_file), train_destination_directory)
        print(f"Moved {txt_file} to {train_destination_directory}")
    # Check if the txt file name matches any mp4 file name in val directory
    elif os.path.splitext(txt_file)[0] in val_mp4_file_names:
        # Move the txt file to the val destination directory
        shutil.move(os.path.join(txt_directory, txt_file), val_destination_directory)
        print(f"Moved {txt_file} to {val_destination_directory}")

# Check for unmatched mp4 files in train directory
for mp4_file in train_mp4_files:
    if os.path.splitext(mp4_file)[0] not in train_mp4_file_names:
        unmatched_mp4_files.append(mp4_file)

# Check for unmatched mp4 files in val directory
for mp4_file in val_mp4_files:
    if os.path.splitext(mp4_file)[0] not in val_mp4_file_names:
        unmatched_mp4_files.append(mp4_file)

# Print unmatched mp4 files
if unmatched_mp4_files:
    print("The following mp4 files do not have corresponding txt files:")
    for mp4_file in unmatched_mp4_files:
        print(mp4_file)
else:
    print("All mp4 files have corresponding txt files.")