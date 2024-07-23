import os
import random
import shutil

def split_data(directory, train_ratio=0.7):
    # List all files in the directory
    files = os.listdir(directory)
    # Shuffle the list of files
    random.shuffle(files)
    
    # Calculate the number of files for training and validation
    num_train = int(len(files) * train_ratio)
    num_val = len(files) - num_train
    
    # Create directories for training and validation data if they don't exist
    train_dir = os.path.join(directory, 'train')
    val_dir = os.path.join(directory, 'val')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    
    # Move files to training directory
    for file in files[:num_train]:
        src = os.path.join(directory, file)
        dst = os.path.join(train_dir, file)
        shutil.move(src, dst)
    
    # Move files to validation directory
    for file in files[num_train:]:
        src = os.path.join(directory, file)
        dst = os.path.join(val_dir, file)
        shutil.move(src, dst)

# Provide the path to your directory containing videos
directory_path = 'vids'

# Call the function to split the data
split_data(directory_path)
