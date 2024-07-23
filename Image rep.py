import cv2
import pandas as pd

# Read the image file
image_path = 'vif_frames/187_1/frame_0131.jpeg'
frame_number_to_display = 131  # Specify the frame number you want to display
frame = cv2.imread(image_path)

# Read the bounding box coordinates from the CSV file
csv_path = 'mot_clean/187_1.txt'
df = pd.read_csv(csv_path)

# Get the bounding box coordinates for the specified frame
frame_boxes = df[df['frame'] == frame_number_to_display]

# Draw bounding boxes on the frame
for _, row in frame_boxes.iterrows():
    x, y, x_offset, y_offset, obj_id = int(row['x']), int(row['y']), int(row['x_offset']), int(row['y_offset']), int(row['id'])
    xmin, ymin, xmax, ymax = x, y, x + x_offset, y + y_offset

    # Draw bounding box
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Display object id
    cv2.putText(frame, f"ID: {obj_id}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the frame with bounding boxes
cv2.imshow('Frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()