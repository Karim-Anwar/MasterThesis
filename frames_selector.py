import cv2
import os

def get_color(idx):
    idx = idx * 3
    color = ((37 * idx) % 255, (17 * idx) % 255, (29 * idx) % 255)
    return color

# Function to draw bounding boxes and IDs on the frame
def draw_bounding_boxes(frame, boxes):
    for box in boxes:
        x, y, w, h, obj_id = map(float, box)
        x, y, w, h = int(x), int(y), int(w), int(h)
        color = get_color(abs(int(obj_id)))
        text_color = (255, 255, 255)  # Color for text (white)

        # Draw the bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=color, thickness=3)
        
        # Draw the object ID
        cv2.putText(frame, str(int(obj_id)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, text_color, 2, cv2.LINE_AA)
        
    return frame

# Function to save specified frames with bounding boxes
def save_frames_with_bounding_boxes(video_path, bbox_results_path, frame_numbers, output_dir):
    # Read bounding box results
    bboxes = {}
    with open(bbox_results_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            frame_num = int(parts[0])
            obj_id = int(parts[1])  # Object ID is the second column
            box = list(map(float, parts[2:6]))  # x1, y1, w, h
            if frame_num not in bboxes:
                bboxes[frame_num] = []
            bboxes[frame_num].append(box + [obj_id])
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for frame_num in frame_numbers:
        if frame_num >= frame_count:
            print(f"Frame number {frame_num} exceeds the total frame count of {frame_count}. Skipping.")
            continue
        
        if frame_num not in bboxes:
            print(f"No bounding boxes found for frame {frame_num}. Skipping.")
            continue

        # Set video to the specified frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame {frame_num}.")
            continue
        
        # Draw bounding boxes and IDs
        frame = draw_bounding_boxes(frame, bboxes[frame_num])
        
        # Save the frame as an image file
        output_path = os.path.join(output_dir, f"frame_{frame_num}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Saved {output_path}")

    cap.release()

# Example usage
video_path = 'FairMOT_ROOT/videos/217_2.mp4'
bbox_results_path = 'FairMOT_ROOT/demos/results.txt'
frame_numbers = [100, 150, 200]  # Example frame numbers
output_dir = 'output_frames/scratch'

save_frames_with_bounding_boxes(video_path, bbox_results_path, frame_numbers, output_dir)
