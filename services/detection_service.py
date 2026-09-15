import cv2
import time
from typing import Dict, Any, Tuple
from core.inference_engine import InferenceEngine
from utils.video_utils import FPSCounter
from utils.image_utils import draw_detections, resize_with_aspect_ratio
from services.camera_service import CameraService
from services.alert_service import AlertService
from database.detection_repository import DetectionRepository
import numpy as np
import config

class DetectionService:
    def __init__(self, camera_service: CameraService, alert_service: AlertService):
        self.camera_service = camera_service
        self.alert_service = alert_service
        self.det_repo = DetectionRepository()
        
        # camera_id -> InferenceEngine
        self.engines: Dict[int, InferenceEngine] = {}
        # camera_id -> FPSCounter
        self.fps_counters: Dict[int, FPSCounter] = {}
        
    def start_detection(self, camera_id: int):
        if camera_id not in self.engines:
            cam_data = self.camera_service.repo.get_camera_by_id(camera_id)
            model_name = cam_data.get('model_name', config.DEFAULT_MODEL_NAME) if cam_data else config.DEFAULT_MODEL_NAME
            model_path = str(config.MODELS_DIR / model_name)
            
            self.engines[camera_id] = InferenceEngine(model_path=model_path)
            self.fps_counters[camera_id] = FPSCounter()
            
        self.camera_service.start_camera(camera_id)

    def stop_detection(self, camera_id: int):
        self.camera_service.stop_camera(camera_id)
        if camera_id in self.engines:
            del self.engines[camera_id]
        if camera_id in self.fps_counters:
            del self.fps_counters[camera_id]

    def process_latest_frame(self, camera_id: int, resize_width: int = 800) -> Tuple[np.ndarray, float]:
        frame = self.camera_service.get_frame(camera_id)
        
        if frame is None:
            return None, 0.0
            
        # Tick FPS
        fps = 0.0
        if camera_id in self.fps_counters:
            fps = self.fps_counters[camera_id].tick()

        engine = self.engines.get(camera_id)
        if engine:
            tracked_detections, alerts = engine.process_frame(frame)
            
            # Log all detections async/fire-and-forget in real system, here we log synchronously
            for det in tracked_detections:
                bbox_str = ",".join(map(str, map(int, det['bbox'])))
                self.det_repo.log_detection(
                    camera_id=camera_id,
                    class_name=det['class_name'],
                    confidence=det['confidence'],
                    bbox=bbox_str,
                    track_id=det.get('track_id')
                )
            
            # Handle triggered alerts
            if alerts:
                cam_data = self.camera_service.repo.get_camera_by_id(camera_id)
                cam_name = cam_data['name'] if cam_data else f"Camera {camera_id}"
                self.alert_service.process_alerts(alerts, camera_id, cam_name, frame.copy())
            
            # Draw overlay
            frame = draw_detections(frame, tracked_detections)
            
            # Draw FPS
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if resize_width:
            frame = resize_with_aspect_ratio(frame, width=resize_width)
            
        return frame, fps
