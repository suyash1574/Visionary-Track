
# Execution Instructions for Visionary Tracker

Used a dataset of VisDrone2019-DET-train
Follow these steps to execute the Visionary Tracker project from scratch. This guide assumes you have a basic understanding of Python and command-line usage.

## Step 1: Clone the Repository
Clone the project repository to your local machine and navigate to the project directory:

```bash
git clone <your-repo-url>
cd visionary_tracker
```

## Step 2: Install Dependencies
Install the required Python packages listed in `requirements.txt`. Ensure you have Python 3.8 or higher installed.

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
ultralytics
opencv-python
torch
torchvision
torchaudio
flask
```

## Step 3: Prepare the Dataset
Place the `VisDrone2019-DET-train` dataset in the `data/raw/VisDrone2019-DET-train/` directory. The structure should look like this:

```
data/raw/VisDrone2019-DET-train/
├── images/
│   ├── 9999974_00000_d_0000053.jpg
│   └── ...
└── annotations/
    ├── 9999974_00000_d_0000053.txt
    └── ...
```

Convert the VisDrone annotations to YOLO format by running the conversion script:

```bash
python src/data/convert.py
```

This generates a `labels/` directory in `data/raw/VisDrone2019-DET-train/` with YOLO-formatted annotations.

## Step 4: Verify Camera Access
Test if your webcam is accessible (skip this if using a video file):

```bash
python src/camera.py
```

### Expected Output:
```
Camera opened successfully with index 0
Successfully read a frame
Successfully read a frame
...
```

If the camera fails to open, check permissions (Settings > Privacy & Security > Camera on Windows) or ensure no other apps are using the camera. Alternatively, use a video file in Step 6.

## Step 5: Train the Model
Train the YOLOv5 model on the VisDrone dataset to fine-tune it for object detection and tracking:

```bash
python src/train.py
```

### Training Details:
- **Model:** YOLOv5s (small version for faster training).
- **Epochs:** 50 (takes ~49 hours on CPU, ~1-2 hours on GPU).
- **Image Size:** 416x416.
- **Batch Size:** 16.
- **Output:** Trained weights are saved in `runs/train/visionary_tracker_train/weights/best.pt`.

**Note:** If training is too slow, reduce epochs to 10 by editing `src/train.py`:

```python
epochs=10
```

## Step 6: Run the Web Demo
Start the Flask server to view the live demo:

```bash
python src/app/app.py
```

Open your browser and go to `http://127.0.0.1:5000`.

You should see a webpage titled **"Visionary Tracker - Live Object Detection and Tracking"** with a live video feed showing detected objects with bounding boxes and tracking IDs.

### If the Webcam Fails:
Modify `src/inference.py` to use a video file instead of the camera:

```python
self.cap = cv2.VideoCapture("path/to/your/test_video.mp4")
```

Replace `path/to/your/test_video.mp4` with a valid video file path, then re-run:

```bash
python src/app/app.py
```

## Step 7: Debug and Test
If the video feed doesn’t show or no objects are detected, debug using the following:

### Test Model Inference
Run the inference test script to check if the model detects objects on a single frame:

```bash
python src/test_inference.py
