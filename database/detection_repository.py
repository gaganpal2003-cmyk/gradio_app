from .connection import get_db_connection
from app_utils.logger import logger
from typing import List, Dict, Any

class DetectionRepository:
    def __init__(self):
        self.db = get_db_connection()

    def log_detection(self, camera_id: int, class_name: str, confidence: float, 
                      bbox: str, track_id: int = None) -> bool:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO detections 
                        (camera_id, class_name, confidence, bbox, track_id) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (camera_id, class_name, confidence, bbox, track_id)
                    )
            return True
        except Exception as e:
            # We don't log every single error here to avoid spamming the logs during high FPS
            return False

    def get_detection_counts_by_class(self, hours: int = 24) -> Dict[str, int]:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT class_name, COUNT(*) as count 
                        FROM detections 
                        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                        GROUP BY class_name
                        """,
                        (hours,)
                    )
                    results = cursor.fetchall()
                    return {r['class_name']: r['count'] for r in results}
        except Exception as e:
            logger.error(f"Error fetching detection counts: {e}")
            return {}

    def get_hourly_trends(self, hours: int = 24) -> List[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as hour, 
                               COUNT(*) as count
                        FROM alerts
                        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                        GROUP BY hour
                        ORDER BY hour ASC
                        """,
                        (hours,)
                    )
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching hourly trends: {e}")
            return []
