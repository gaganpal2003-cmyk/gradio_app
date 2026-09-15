import cv2
import time
from collections import deque
from typing import Union, Tuple

def validate_video_source(source: Union[str, int], timeout_seconds: float = 3.0) -> Tuple[bool, str]:
    """
    Validates if a video source (RTSP, webcam index, or file) can be opened.
    Returns (is_valid, message).
    """
    try:
        # Check if source is integer (webcam index)
        if isinstance(source, str) and source.isdigit():
            source = int(source)

        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            return False, f"Could not connect to video source: {source}"

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return False, f"Connected to {source}, but failed to read initial frame."

        h, w = frame.shape[:2]
        return True, f"Success: Connected to {source} ({w}x{h} resolution)"
    except Exception as e:
        return False, f"Error validating source: {str(e)}"

class FPSCounter:
    """Rolling window FPS calculator."""
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.timestamps = deque(maxlen=window_size)

    def tick(self) -> float:
        now = time.time()
        self.timestamps.append(now)
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        if elapsed <= 0:
            return 0.0
        return (len(self.timestamps) - 1) / elapsed

    @property
    def fps(self) -> float:
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        if elapsed <= 0:
            return 0.0
        return (len(self.timestamps) - 1) / elapsed

def calculate_fps(prev_time: float) -> Tuple[float, float]:
    current_time = time.time()
    delta = current_time - prev_time
    fps = 1.0 / delta if delta > 0 else 0.0
    return fps, current_time
