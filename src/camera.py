import cv2

for index in range(5):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"Camera opened successfully with index {index}")
        for _ in range(10):  # Read 10 frames
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break
            print(f"Frame shape: {frame.shape}")
        cap.release()
        break
    else:
        print(f"Failed to open camera with index {index}")
        cap.release()