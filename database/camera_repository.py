from .connection import get_db_connection
from utils.logger import logger
from typing import List, Dict, Any, Optional

class CameraRepository:
    def __init__(self):
        self.db = get_db_connection()

    def get_all_cameras(self, active_only: bool = False) -> List[Dict[str, Any]]:
        query = "SELECT * FROM cameras"
        if active_only:
            query += " WHERE is_active = TRUE"
        
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching cameras: {e}")
            return []

    def get_camera_by_id(self, camera_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM cameras WHERE id = %s", (camera_id,))
                    return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching camera {camera_id}: {e}")
            return None

    def add_camera(self, name: str, source: str, location: str = "Main Facility", 
                   model_name: str = "ppe.pt", conf_threshold: float = 0.35) -> bool:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO cameras (name, source, location, model_name, conf_threshold) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (name, source, location, model_name, conf_threshold)
                    )
            return True
        except Exception as e:
            logger.error(f"Error adding camera: {e}")
            return False

    def update_camera(self, camera_id: int, **kwargs) -> bool:
        if not kwargs:
            return True
            
        set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = list(kwargs.values())
        values.append(camera_id)
        
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"UPDATE cameras SET {set_clause} WHERE id = %s", tuple(values))
            return True
        except Exception as e:
            logger.error(f"Error updating camera {camera_id}: {e}")
            return False

    def delete_camera(self, camera_id: int) -> bool:
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM cameras WHERE id = %s", (camera_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting camera {camera_id}: {e}")
            return False
