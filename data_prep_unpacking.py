import os
import shutil
import glob
import cv2
import os

videos_directory = 'vids/train'  # Replace with the directory containing the videos
frames_directory = 'FairMOT_ROOT/src/data/fish/images/train'  # Replace with the directory where frames will be saved

video_files = sorted([f for f in os.listdir(videos_directory) if f.endswith('.mp4')])  # Get a sorted list of video files

frame_count = 1  # Initialize the frame count

for video_file in video_files:
    print(f"Processing video: {video_file}")  # Print the name of the video being processed
    video_path = os.path.join(videos_directory, video_file)
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    while success:
        frame_path = os.path.join(frames_directory, f'{frame_count:05d}.jpg')
        cv2.imwrite(frame_path, image)  # Save frame as JPEG file
        success, image = vidcap.read()
        frame_count += 1

vidcap.release()
cv2.destroyAllWindows()