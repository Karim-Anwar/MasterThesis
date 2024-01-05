import cv2
import os

def extract_frames(video_path, output_root_folder):
    # List all video files in the video path
    video_files = [f for f in os.listdir(video_path) if f.endswith(('.mp4', '.avi', '.mkv'))]

    for video_file in video_files:
        # Construct the full path for the video file
        video_file_path = os.path.join(video_path, video_file)

        # Create a folder for each video using its name
        video_name = os.path.splitext(video_file)[0]
        output_folder = os.path.join(output_root_folder, video_name)

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the video file
        cap = cv2.VideoCapture(video_file_path)

        # Check if the video is successfully opened
        if not cap.isOpened():
            print(f"Error opening video file: {video_file_path}")
            continue

        # Get video properties
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        print(f"Processing Video: {video_file}, Frames: {frame_count}, FPS: {fps}")

        # Loop through each frame and save it as an image
        for frame_number in range(frame_count):
            ret, frame = cap.read()

            if not ret:
                print(f"Error reading frame {frame_number} from video {video_file}.")
                break

            # Save the frame as an image
            frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpeg")
            cv2.imwrite(frame_filename, frame)

        # Release the video capture object
        cap.release()

if __name__ == "__main__":
    video_path = "vids"  # Use a raw string to avoid issues
    output_root_folder = "vif_frames"  # Use a raw string to avoid issues

    extract_frames(video_path, output_root_folder)
