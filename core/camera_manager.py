import cv2
import threading
import time
from typing import Optional
from utils.logger import logger
import numpy as np

class CameraManager:
    """
    Manages a background thread to continuously capture frames from a video source.
    Prevents the main thread from blocking due to network latency (RTSP).
    Maintains a buffer of the most recent frame.
    """
    def __init__(self, source: str, camera_id: int):
        if source.isdigit():
            self.source = int(source)
        else:
            self.source = source
        self.camera_id = camera_id
        
        self.cap = None
        self.is_running = False
        self.thread = None
        self.current_frame = None
        self.lock = threading.Lock()
        
    def start(self):
        if self.is_running:
            return
        
        self.cap = cv2.VideoCapture(self.source)
        # Attempt to lower buffer size for RTSP to reduce latency
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        
        if not self.cap.isOpened():
            logger.error(f"CameraManager [{self.camera_id}]: Failed to open source {self.source}")
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        logger.info(f"CameraManager [{self.camera_id}]: Started thread for {self.source}")

    def _update(self):
        reconnect_attempts = 0
        while self.is_running:
            if not self.cap.isOpened():
                if reconnect_attempts < 5:
                    logger.warning(f"CameraManager [{self.camera_id}]: Reconnecting...")
                    time.sleep(2)
                    self.cap.open(self.source)
                    reconnect_attempts += 1
                else:
                    logger.error(f"CameraManager [{self.camera_id}]: Reconnect failed.")
                    self.is_running = False
                    break
                continue

            ret, frame = self.cap.read()
            if not ret or frame is None:
                # End of video file or stream dropped
                time.sleep(0.01)
                continue
                
            reconnect_attempts = 0
            with self.lock:
                self.current_frame = frame.copy()
                
            # Optional: sleep slightly to not max out CPU for very high FPS local cameras
            time.sleep(0.005)

    def read(self) -> Optional[np.ndarray]:
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        if self.cap is not None:
            self.cap.release()
        logger.info(f"CameraManager [{self.camera_id}]: Stopped thread.")
