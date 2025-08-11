import cv2
import torch
import numpy as np
import config

# Camera and object detection functionality.
class VisionSystem:
    def __init__(self):
        # Load YOLOv5 'nano' model, efficient on low end.
        print("Loading YOLOv5 model...")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
        self.model.classes = [0]  # Filter for 'person' class (ID 0) only.
        self.model.conf = config.CONFIDENCE_THRESHOLD
        print("Model loaded.")
        
        # Initialize camera capture object.
        print("Initializing camera...")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        print("Camera initialized.")

    # Fetches and resizes single frame from camera.
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize for consistent processing dimensions.
            frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        return ret, frame

    # Runs inference on frame to find human target.
    def find_target(self, frame):
        # Convert BGR frame from OpenCV to RGB for the PyTorch model.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        detections = results.pandas().xyxy[0]
        person_detections = detections[detections['name'] == 'person']

        if not person_detections.empty:
            # If multiple people found, select one with the largest bounding box area.
            # finds 'closest' or 'largest' target.
            person_detections['area'] = (person_detections['xmax'] - person_detections['xmin']) * \
                                        (person_detections['ymax'] - person_detections['ymin'])
            target = person_detections.loc[person_detections['area'].idxmax()]
            return target
        
        # No person detected in the frame.
        return None

    # Releases camera resource.
    def release(self):
        print("Releasing camera resource.")
        self.cap.release()