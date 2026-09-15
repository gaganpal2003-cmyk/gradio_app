from .connection import get_db_connection
from app_utils.logger import logger
from typing import List, Dict, Any, Optional

class AlertRepository:
    def __init__(self):
        self.db = get_db_connection()

    def create_alert(self, camera_id: int, camera_name: str, violation_type: str, 
                     severity: str, confidence: float, track_id: Optional[int], 
                     snapshot_path: Optional[str]) -> bool:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO alerts 
                        (camera_id, camera_name, violation_type, severity, confidence, track_id, snapshot_path) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (camera_id, camera_name, violation_type, severity, confidence, track_id, snapshot_path)
                    )
            return True
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return False

    def get_alerts(self, limit: int = 50, camera_id: int = None, severity: str = None, 
                   status: str = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if camera_id is not None:
            query += " AND camera_id = %s"
            params.append(camera_id)
        if severity:
            query += " AND severity = %s"
            params.append(severity)
        if status:
            query += " AND status = %s"
            params.append(status)

        query += " ORDER BY timestamp DESC LIMIT %s"
        params.append(limit)

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(params))
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching alerts: {e}")
            return []

    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.get_alerts(limit=limit)

    def update_alert_status(self, alert_id: int, status: str) -> bool:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE alerts SET status = %s WHERE id = %s", (status, alert_id))
            return True
        except Exception as e:
            logger.error(f"Error updating alert status: {e}")
            return False

    def get_alert_stats(self) -> Dict[str, Any]:
        """Returns total alerts today and critical alerts count."""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as count FROM alerts WHERE DATE(timestamp) = CURDATE()"
                    )
                    today_alerts = cursor.fetchone()['count']

                    cursor.execute(
                        "SELECT COUNT(*) as count FROM alerts WHERE severity = 'CRITICAL' AND status = 'UNRESOLVED'"
                    )
                    critical_alerts = cursor.fetchone()['count']

                    return {
                        "today": today_alerts,
                        "unresolved_critical": critical_alerts
                    }
        except Exception as e:
            logger.error(f"Error fetching alert stats: {e}")
            return {"today": 0, "unresolved_critical": 0}
