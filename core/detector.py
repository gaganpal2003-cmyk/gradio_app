import os
import torch
from typing import List, Dict, Any, Union
from app_utils.logger import logger
import config

class Detector:
    def __init__(self, model_path: str = None, conf_threshold: float = None):
        self.model_path = model_path or config.DEFAULT_MODEL_PATH
        self.conf_threshold = conf_threshold if conf_threshold is not None else config.CONF_THRESHOLD
        self.model = None
        self.model_type = None # "yolov5" or "yolov8"
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return

        try:
            # 1. Try loading as Ultralytics YOLOv8/v11
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            self.model_type = "yolov8"
            logger.info(f"Loaded YOLOv8+ model: {self.model_path}")
            return
        except Exception as e:
            logger.warning(f"Failed to load as YOLOv8 (might be YOLOv5 checkpoint): {e}")

        try:
            # 2. Fallback to YOLOv5 Torch Hub loader
            logger.info("Attempting to load via torch.hub YOLOv5...")
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path, force_reload=False)
            self.model.conf = self.conf_threshold
            self.model.iou = config.IOU_THRESHOLD
            self.model_type = "yolov5"
            logger.info(f"Loaded YOLOv5 model via torch hub: {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_path} via any engine: {e}")

    def predict(self, frame) -> List[Dict[str, Any]]:
        """
        Runs inference on the frame and returns standardized detection list.
        [{'bbox': [x1,y1,x2,y2], 'confidence': 0.95, 'class_name': 'helmet'}]
        """
        if self.model is None or frame is None:
            return []

        results_list = []
        try:
            if self.model_type == "yolov8":
                results = self.model(frame, conf=self.conf_threshold, iou=config.IOU_THRESHOLD, verbose=False)
                if not results:
                    return []
                
                boxes = results[0].boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0].cpu().numpy())
                        cls_id = int(box.cls[0].cpu().numpy())
                        cls_name = self.model.names[cls_id]
                        
                        results_list.append({
                            "bbox": [x1, y1, x2, y2],
                            "confidence": conf,
                            "class_name": cls_name
                        })

            elif self.model_type == "yolov5":
                # YOLOv5 torch hub returns Pandas dataframe
                results = self.model(frame)
                df = results.pandas().xyxy[0]
                
                for _, row in df.iterrows():
                    conf = float(row['confidence'])
                    if conf >= self.conf_threshold:
                        results_list.append({
                            "bbox": [row['xmin'], row['ymin'], row['xmax'], row['ymax']],
                            "confidence": conf,
                            "class_name": row['name']
                        })

        except Exception as e:
            logger.error(f"Inference error: {e}")
            
        return results_list
