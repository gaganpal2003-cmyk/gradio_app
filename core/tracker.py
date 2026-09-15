import math
from typing import List, Dict, Any

class SimpleTracker:
    """
    A simple centroid-based tracker to maintain consistent IDs across frames.
    Prevents alert spamming by tracking objects for cooldown periods.
    """
    def __init__(self, max_distance: float = 50.0, max_disappeared: int = 15):
        self.next_object_id = 1
        self.objects = {}       # id -> centroid (cx, cy)
        self.disappeared = {}   # id -> consecutive frames not seen
        self.max_distance = max_distance
        self.max_disappeared = max_disappeared

    def _get_centroid(self, bbox: List[float]) -> tuple:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not detections:
            # If no detections, increment disappeared counter for all objects
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)
            return []

        input_centroids = [self._get_centroid(d["bbox"]) for d in detections]
        
        if not self.objects:
            for i, centroid in enumerate(input_centroids):
                self._register(centroid)
                detections[i]["track_id"] = self.next_object_id - 1
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            # Distance matrix
            D = [[math.dist(c1, c2) for c2 in input_centroids] for c1 in object_centroids]
            
            used_rows = set()
            used_cols = set()

            # Greedy matching
            for _ in range(min(len(object_ids), len(input_centroids))):
                min_val = float('inf')
                min_row = -1
                min_col = -1
                for r in range(len(object_ids)):
                    if r in used_rows: continue
                    for c in range(len(input_centroids)):
                        if c in used_cols: continue
                        if D[r][c] < min_val:
                            min_val = D[r][c]
                            min_row = r
                            min_col = c

                if min_row == -1 or min_val > self.max_distance:
                    break
                    
                object_id = object_ids[min_row]
                self.objects[object_id] = input_centroids[min_col]
                self.disappeared[object_id] = 0
                detections[min_col]["track_id"] = object_id
                
                used_rows.add(min_row)
                used_cols.add(min_col)

            # Register unmatched inputs
            for c in range(len(input_centroids)):
                if c not in used_cols:
                    self._register(input_centroids[c])
                    detections[c]["track_id"] = self.next_object_id - 1

            # Increment disappeared for unmatched existing objects
            for r in range(len(object_ids)):
                if r not in used_rows:
                    obj_id = object_ids[r]
                    self.disappeared[obj_id] += 1
                    if self.disappeared[obj_id] > self.max_disappeared:
                        self._deregister(obj_id)

        return detections

    def _register(self, centroid: tuple):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def _deregister(self, object_id: int):
        del self.objects[object_id]
        del self.disappeared[object_id]
