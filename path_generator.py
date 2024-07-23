import os

def find_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png']  # Add more extensions if needed
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    return image_files

def write_to_file(file_list, output_file):
    with open(output_file, 'w') as f:
        for file_path in file_list:
            f.write(file_path + '\n')

if __name__ == "__main__":
    directory_to_search = '/mnt/d/Documents/Thesis Transformer/FairMOT_ROOT/src/lib/datasets/dataset/sanity/images2'
    output_file_path = 'FairMOT_ROOT/src/data/sanity2.train'

    images = find_images(directory_to_search)
    write_to_file(images, output_file_path)

    print("Image paths written to", output_file_path)
