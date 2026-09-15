import cv2
import numpy as np
import base64
from typing import List, Dict, Any, Tuple
from PIL import Image
import io

# Color palette (BGR format for OpenCV)
COLOR_VIOLATION = (0, 0, 235)      # Vivid Red
COLOR_COMPLIANT = (50, 205, 50)    # Lime Green
COLOR_NEUTRAL = (235, 160, 52)     # Sky Blue
COLOR_WARNING = (0, 165, 255)      # Orange

def get_class_color(class_name: str) -> Tuple[int, int, int]:
    lower = class_name.lower()
    if lower.startswith("no_") or "violation" in lower:
        return COLOR_VIOLATION
    elif any(comp in lower for comp in ["helmet", "vest", "shoe", "boot", "compliant"]):
        return COLOR_COMPLIANT
    elif "truck" in lower or "window" in lower or "car" in lower:
        return COLOR_WARNING
    return COLOR_NEUTRAL

def draw_detections(
    frame: np.ndarray,
    detections: List[Dict[str, Any]],
    show_labels: bool = True,
    show_conf: bool = True
) -> np.ndarray:
    """
    Draws bounding boxes and stylized badges on the image frame.
    Detections format: list of dicts with 'bbox' [x1, y1, x2, y2], 'class_name', 'confidence', optional 'track_id'.
    """
    if frame is None or len(detections) == 0:
        return frame

    annotated = frame.copy()
    h, w = annotated.shape[:2]

    for det in detections:
        bbox = det.get("bbox", [])
        if len(bbox) < 4:
            continue
        x1, y1, x2, y2 = [int(v) for v in bbox[:4]]
        # Clamp bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)

        cls_name = det.get("class_name", "Object")
        conf = det.get("confidence", 0.0)
        track_id = det.get("track_id", None)
        color = get_class_color(cls_name)

        # Draw rounded or sleek box border
        thickness = 2 if max(h, w) < 1200 else 3
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

        if show_labels:
            # Build label text
            label = cls_name.replace("_", " ").title()
            if track_id is not None:
                label = f"#{track_id} {label}"
            if show_conf:
                label = f"{label} {conf:.2f}"

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

            # Draw background tag
            tag_y1 = max(0, y1 - text_h - baseline - 6)
            tag_y2 = y1
            tag_x1 = x1
            tag_x2 = min(w, x1 + text_w + 10)

            # Draw filled rectangle for badge background
            cv2.rectangle(annotated, (tag_x1, tag_y1), (tag_x2, tag_y2), color, -1)
            # Text inside badge (white or dark depending on color)
            cv2.putText(
                annotated,
                label,
                (tag_x1 + 5, tag_y2 - baseline - 2),
                font,
                font_scale,
                (255, 255, 255),
                font_thickness,
                cv2.LINE_AA
            )

    return annotated

def resize_with_aspect_ratio(image: np.ndarray, width: int = None, height: int = None, inter=cv2.INTER_AREA) -> np.ndarray:
    if image is None:
        return None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)

def encode_image_base64(image: np.ndarray) -> str:
    """Converts BGR image numpy array to base64 JPEG string."""
    if image is None:
        return ""
    success, buffer = cv2.imencode(".jpg", image)
    if not success:
        return ""
    return base64.b64encode(buffer).decode("utf-8")
