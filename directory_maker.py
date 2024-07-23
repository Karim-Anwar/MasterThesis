import os
import shutil

# Function to create directories and move files
def organize_videos(directory):
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Check if the file is a video file (you can extend this condition based on your specific requirements)
        if os.path.isfile(filepath) and filename.lower().endswith(('.txt')):
            # Extract the name of the file without extension
            file_name = os.path.splitext(filename)[0]
            # Create a directory with the same name as the file if it doesn't exist
            dest_directory = os.path.join(directory, file_name)
            if not os.path.exists(dest_directory):
                os.makedirs(dest_directory)
            # Move the file into the directory
            shutil.move(filepath, os.path.join(dest_directory, filename))

# Specify the directory containing the video files
video_directory = r'mot_clean\val'

# Call the function to organize the videos
organize_videos(video_directory)
