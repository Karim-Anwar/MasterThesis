import os

main_dir = r'mot_clean\train'
output_dir = r'FairMOT_ROOT\src\lib\datasets\dataset\fish\labels_with_ids\train'
width = 1920
height = 1080


# Iterate through each subdirectory in the main directory
for root, _, files in os.walk(main_dir):
    frame_counter = 1  # Initialize the frame counter
    for file_name in files:
        if file_name.endswith(".txt"):  # Process only text files
            file_path = os.path.join(root, file_name)
            output_subdir = os.path.join(output_dir, os.path.splitext(file_name)[0])  # Create subdir based on file name

            # Create the directory if it doesn't exist
            os.makedirs(output_subdir, exist_ok=True)

            print(f"Processing file: {file_path}")

            # Read the Text File
            with open(file_path, 'r') as file:
                lines = file.readlines()[1:]

            # Split the Lines by Frame
            frame_objects = {}
            for line in lines:
                frame, id, x_min, y_min, x_offset, y_offset = [float(val) for val in line.split(',')]

                if frame not in frame_objects:
                    frame_objects[frame] = []
                frame_objects[frame].append((id, x_min, y_min, x_offset, y_offset))

            # Calculate New Columns
            output_data = {}
            for frame, objects in sorted(frame_objects.items()):
                frame_data = []
                for obj in objects:
                    id, x_min, y_min, x_offset, y_offset = obj
                    id = int(id) - 1
                    x_center = ((x_min + (x_min + x_offset)) / 2) / width
                    y_center = ((y_min + (y_min + y_offset)) / 2) / height
                    w = x_offset / width
                    h = y_offset / height
                    frame_data.append((0, id, x_center, y_center, w, h))
                output_data[frame] = frame_data

            # Save the output data to new text files in the target directory
            for frame in sorted(output_data.keys()):
                new_file_path = os.path.join(output_subdir, f"{os.path.splitext(os.path.basename(file_path))[0]}_{frame_counter}.txt")  # Format the file name as 00001.txt ... 0000N.txt
                with open(new_file_path, "w") as new_file:
                    for data in output_data[frame]:
                        new_file.write(' '.join(str(val) for val in data) + '\n')  # Write the data to the new file without parentheses
                frame_counter += 1  # Increment the frame counter for the next file
