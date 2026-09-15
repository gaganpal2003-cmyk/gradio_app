import os
import cv2
import uuid
from typing import List, Dict, Any
from database.alert_repository import AlertRepository
from app_utils.image_utils import draw_detections
from app_utils.logger import logger
import config

class AlertService:
    def __init__(self):
        self.repo = AlertRepository()

    def process_alerts(self, alerts: List[Dict[str, Any]], camera_id: int, camera_name: str, frame):
        """
        Takes raw triggered alerts, draws a snapshot, saves to disk, and records to database.
        """
        if not alerts or frame is None:
            return

        # Draw ALL detections from these alerts clearly on the snapshot
        # For snapshot, we might want to highlight ONLY the violations.
        annotated_frame = draw_detections(frame, alerts)
        
        # Save snapshot once for this batch of alerts
        snapshot_filename = f"{camera_id}_{uuid.uuid4().hex[:8]}.jpg"
        snapshot_path = str(config.ALERTS_DIR / snapshot_filename)
        
        try:
            cv2.imwrite(snapshot_path, annotated_frame)
            relative_snapshot_path = f"data/alerts/{snapshot_filename}"
        except Exception as e:
            logger.error(f"Failed to save alert snapshot: {e}")
            relative_snapshot_path = None

        # Record each alert in DB
        for det in alerts:
            cls_name = det.get('class_name', 'unknown')
            conf = det.get('confidence', 0.0)
            track_id = det.get('track_id')
            
            # Simple severity logic
            severity = 'HIGH'
            if 'helmet' in cls_name.lower():
                severity = 'CRITICAL'
                
            self.repo.create_alert(
                camera_id=camera_id,
                camera_name=camera_name,
                violation_type=cls_name,
                severity=severity,
                confidence=conf,
                track_id=track_id,
                snapshot_path=relative_snapshot_path
            )

    def get_recent_alerts(self, limit=50, camera_id=None, severity=None, status=None):
        return self.repo.get_alerts(limit=limit, camera_id=camera_id, severity=severity, status=status)

    def update_alert_status(self, alert_id: int, status: str) -> bool:
        return self.repo.update_alert_status(alert_id, status)
