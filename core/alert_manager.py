import time
from typing import List, Dict, Any
from app_utils.logger import logger
import config

class AlertManager:
    """
    Evaluates detections against alert rules, preventing duplicate alerts
    for the same object track ID within a cooldown period.
    """
    def __init__(self):
        self.cooldown_seconds = config.ALERT_COOLDOWN_SECONDS
        self.violation_classes = config.VIOLATION_CLASSES
        self.last_alert_time = {} # track_id -> timestamp

    def evaluate(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Returns a list of detections that should trigger an alert.
        """
        triggered_alerts = []
        now = time.time()
        
        for det in detections:
            cls_name = det.get("class_name", "").lower()
            track_id = det.get("track_id")
            
            # Check if this class is considered a violation
            is_violation = False
            if cls_name in self.violation_classes:
                is_violation = True
            elif "no_" in cls_name or "violation" in cls_name:
                is_violation = True

            if is_violation and track_id is not None:
                last_time = self.last_alert_time.get(track_id, 0)
                if (now - last_time) >= self.cooldown_seconds:
                    triggered_alerts.append(det)
                    self.last_alert_time[track_id] = now
                    logger.info(f"Alert triggered for track #{track_id} ({cls_name})")

        # Cleanup old tracks to prevent memory leak
        self._cleanup_old_tracks(now)
        return triggered_alerts

    def _cleanup_old_tracks(self, now: float):
        keys_to_remove = []
        for tid, last_time in self.last_alert_time.items():
            # If we haven't alerted for this track in 3x cooldown, it's likely gone
            if now - last_time > (self.cooldown_seconds * 3):
                keys_to_remove.append(tid)
        
        for tid in keys_to_remove:
            del self.last_alert_time[tid]
