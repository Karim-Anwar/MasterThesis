import os
import shutil
import cv2

# Function to split video into frames
def split_video_into_frames(video_directory, output_directory):
    # Iterate over directories in the video directory
    for dir_name in os.listdir(video_directory):
        dir_path = os.path.join(video_directory, dir_name)
        # Check if it's a directory
        if os.path.isdir(dir_path):
            # Create a corresponding directory in the output directory
            output_dir_path = os.path.join(output_directory, dir_name)
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
            # Iterate over files in the directory
            for filename in os.listdir(dir_path):
                filepath = os.path.join(dir_path, filename)
                # Check if the file is a video file (you can extend this condition based on your specific requirements)
                if os.path.isfile(filepath) and filename.lower().endswith(('.mp4', '.avi', '.mkv')):
                    # Call function to split video into frames
                    split_video(filepath, output_dir_path)

# Function to split video into frames
def split_video(video_path, output_directory):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    # Read the video frame by frame
    frame_count = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Save the frame as an image
        frame_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_{frame_count}.jpg"
        frame_path = os.path.join(output_directory, frame_filename)
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    # Release the video capture object
    cap.release()

# Specify the directory containing the videos with directories having the same names
video_directory = r'vids\train'
# Specify the output directory where the copied directories and frames should be stored
output_directory = r'FairMOT_ROOT\src\lib\datasets\dataset\fish\images\train'

# Call the function to split videos into frames
split_video_into_frames(video_directory, output_directory)
