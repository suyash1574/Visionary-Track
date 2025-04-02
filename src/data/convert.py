import os
import glob

def convert_visdrone_to_yolo(input_path, output_path, image_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for annotation_file in glob.glob(os.path.join(input_path, "*.txt")):
        with open(annotation_file, 'r') as f:
            lines = f.readlines()

        # Get corresponding image file to determine dimensions
        image_name = os.path.splitext(os.path.basename(annotation_file))[0] + ".jpg"
        image_file = os.path.join(image_path, image_name)
        if not os.path.exists(image_file):
            print(f"Image not found: {image_file}, skipping...")
            continue

        # Load image to get dimensions
        import cv2
        img = cv2.imread(image_file)
        if img is None:
            print(f"Failed to load image: {image_file}, skipping...")
            continue
        height, width, _ = img.shape

        # Convert annotations
        label_file = os.path.join(output_path, os.path.basename(annotation_file))
        with open(label_file, 'w') as f:
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue

                # Remove trailing commas and split
                line = line.rstrip(',')
                parts = line.split(',')
                
                # Ensure the line has exactly 8 parts and none of the critical parts are empty
                if len(parts) != 8:
                    print(f"Invalid line in {annotation_file}: {line}, expected 8 parts, got {len(parts)}, skipping...")
                    continue
                if not all(part for part in parts[:6]):  # Check first 6 parts (bbox, score, category)
                    print(f"Invalid line in {annotation_file}: {line}, empty critical field, skipping...")
                    continue

                try:
                    x, y, w, h, score, category, truncation, occlusion = map(int, parts)
                    if category == 0:  # Ignore category 0 (ignored regions)
                        continue
                    # Map VisDrone class IDs (1-11) to YOLO class IDs (0-10)
                    category = category - 1  # Adjust to 0-based index
                    if category > 10:  # Should not happen, but log if it does
                        print(f"Invalid category {category + 1} in {annotation_file}: {line}, skipping...")
                        continue

                    # Convert to YOLO format: <class> <x_center> <y_center> <width> <height> (normalized)
                    x_center = (x + w / 2) / width
                    y_center = (y + h / 2) / height
                    w_norm = w / width
                    h_norm = h / height

                    f.write(f"{category} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
                except ValueError as e:
                    print(f"Error parsing line in {annotation_file}: {line}, error: {e}, skipping...")
                    continue

if __name__ == "__main__":
    input_path = "data/raw/VisDrone2019-DET-train/annotations"
    output_path = "data/raw/VisDrone2019-DET-train/labels"
    image_path = "data/raw/VisDrone2019-DET-train/images"
    convert_visdrone_to_yolo(input_path, output_path, image_path)