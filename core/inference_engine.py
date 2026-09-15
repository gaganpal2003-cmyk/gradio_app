from typing import List, Dict, Any, Tuple
import numpy as np
from core.detector import Detector
from core.tracker import SimpleTracker
from core.alert_manager import AlertManager

class InferenceEngine:
    """
    Coordinates Detector, Tracker, and AlertManager per frame.
    """
    def __init__(self, model_path: str = None, conf_threshold: float = None):
        self.detector = Detector(model_path, conf_threshold)
        self.tracker = SimpleTracker()
        self.alert_manager = AlertManager()

    def process_frame(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Runs the full AI pipeline on a single frame.
        Returns: (all_detections_with_tracks, new_triggered_alerts)
        """
        if frame is None:
            return [], []

        # 1. Detect
        detections = self.detector.predict(frame)

        # 2. Track
        tracked_detections = self.tracker.update(detections)

        # 3. Evaluate Alerts
        alerts = self.alert_manager.evaluate(tracked_detections)

        return tracked_detections, alerts
