import os
import json

def denormalize_bbox(x_norm, y_norm, x_offset_norm, y_offset_norm, img_width, img_height):
    # Denormalize bounding box coordinates
    x = x_norm * img_width
    y = y_norm * img_height
    x_offset = x_offset_norm * img_width
    y_offset = y_offset_norm * img_height
    return x, y, x_offset, y_offset

def convert_to_coco(images_folder, annotations_folder):
    coco_data = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    categories = {}
    category_id = 1
    image_id = 1
    annotations = []

    # Recursively process each image and its corresponding annotation file in the annotations folder
    for root, dirs, files in os.walk(annotations_folder):
        for filename in files:
            if filename.endswith(".txt"):
                annotation_file = os.path.join(root, filename)
                image_file = os.path.join(images_folder, os.path.relpath(root, annotations_folder), filename.replace(".txt", ".jpg"))

                # Extract only the file name from the image file path
                image_filename = os.path.basename(image_file)

                # Read corresponding annotation file
                with open(annotation_file, 'r') as f:
                    lines = f.readlines()

                # Process each annotation line
                for line in lines:
                    data = line.strip().split(' ')
                    class_name, _, x_norm, y_norm, x_offset_norm, y_offset_norm = data

                    # Create category if not exists
                    if class_name not in categories:
                        categories[class_name] = category_id
                        coco_data["categories"].append({
                            "id": category_id,
                            "name": class_name,
                            "supercategory": "object"
                        })
                        category_id += 1

                    image_width, image_height = 1920, 1080  # Replace with actual image dimensions

                    # Denormalize bounding box coordinates
                    x, y, x_offset, y_offset = denormalize_bbox(
                        float(x_norm), float(y_norm), float(x_offset_norm), float(y_offset_norm),
                        image_width, image_height
                    )

                    # Create image data
                    image_data = {
                        "id": image_id,
                        "width": image_width,
                        "height": image_height,
                        "file_name": image_filename,  # Use the extracted file name
                        "license": 1,
                        "flickr_url": "",
                        "coco_url": "",
                        "date_captured": ""
                    }

                    coco_data["images"].append(image_data)

                    # Create annotation data
                    annotation = {
                        "id": len(annotations) + 1,
                        "image_id": image_id,
                        "category_id": categories[class_name],
                        "bbox": [x, y, x_offset, y_offset],
                        "area": x_offset * y_offset,
                        "iscrowd": 0
                    }

                    annotations.append(annotation)

                image_id += 1

    coco_data["annotations"] = annotations

    return coco_data

# Example usage
images_folder_path = "sanity/val"
annotations_folder_path = "sanity/val/annots"
coco_data = convert_to_coco(images_folder_path, annotations_folder_path)

# Save COCO data to a JSON file
output_file = "annotations.json"
with open(output_file, "w") as outfile:
    json.dump(coco_data, outfile)

print(f"COCO annotations saved to {output_file}")
