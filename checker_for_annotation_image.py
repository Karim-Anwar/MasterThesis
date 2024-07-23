import os

def get_file_names(directory, extension):
    """
    Get a list of file names with a specific extension in a directory and its subdirectories.
    """
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_names.append(os.path.splitext(file)[0])
    return file_names

# Define the directories
mp4_directory = 'vids'
txt_directory = 'mots'

# Get a list of mp4 file names
mp4_file_names = get_file_names(mp4_directory, '.mp4')

# Get a list of txt file names
txt_file_names = get_file_names(txt_directory, '.txt')

# Find mp4 files without corresponding txt files
mp4_without_txt = [mp4 for mp4 in mp4_file_names if mp4 not in txt_file_names]

# Find txt files without corresponding mp4 files
txt_without_mp4 = [txt for txt in txt_file_names if txt not in mp4_file_names]

# Output results
print("MP4 files without corresponding TXT files:")
print(mp4_without_txt)

print("\nTXT files without corresponding MP4 files:")
print(txt_without_mp4)
