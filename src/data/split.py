import os
import random
import shutil

# Define paths
raw_data_dir = r"D:\Projects\Visionary tracker\visionary tracker\data\raw\VisDrone2019-DET-train"
images_dir = os.path.join(raw_data_dir, "images")
annotations_dir = os.path.join(raw_data_dir, "annotations")

# Create directories for train and val splits
train_images_dir = r"D:\Projects\Visionary tracker\visionary tracker\data\processed\train\images"
val_images_dir = r"D:\Projects\Visionary tracker\visionary tracker\data\processed\val\images"
train_annotations_dir = r"D:\Projects\Visionary tracker\visionary tracker\data\processed\train\annotations"
val_annotations_dir = r"D:\Projects\Visionary tracker\visionary tracker\data\processed\val\annotations"

os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_annotations_dir, exist_ok=True)
os.makedirs(val_annotations_dir, exist_ok=True)

# Get list of all image filenames
image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]

# Shuffle the list of image files for randomness
random.shuffle(image_files)

# Split into 70% train and 30% validation
train_size = int(0.7 * len(image_files))
train_files = image_files[:train_size]
val_files = image_files[train_size:]

# Function to move images and annotations
def move_files(file_list, source_dir, target_dir):
    for file_name in file_list:
        # Move image file
        shutil.copy(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))

# Move the train and val images
move_files(train_files, images_dir, train_images_dir)
move_files(val_files, images_dir, val_images_dir)

# Move the corresponding annotation files
def move_annotations(file_list, annotations_dir, target_annotations_dir):
    for file_name in file_list:
        annotation_file = file_name.replace('.jpg', '.txt')  # Assuming annotations are .txt files
        shutil.copy(os.path.join(annotations_dir, annotation_file), os.path.join(target_annotations_dir, annotation_file))

# Move the train and val annotations
move_annotations(train_files, annotations_dir, train_annotations_dir)
move_annotations(val_files, annotations_dir, val_annotations_dir)

print(f"Data split completed. Train and validation data saved.")
