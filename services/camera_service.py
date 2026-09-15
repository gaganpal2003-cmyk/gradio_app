from typing import Dict, Any, List, Optional
from core.camera_manager import CameraManager
from database.camera_repository import CameraRepository
from app_utils.logger import logger
import numpy as np

class CameraService:
    def __init__(self):
        self.repo = CameraRepository()
        self.active_managers: Dict[int, CameraManager] = {}

    def start_camera(self, camera_id: int) -> bool:
        if camera_id in self.active_managers:
            return True

        camera_data = self.repo.get_camera_by_id(camera_id)
        if not camera_data:
            logger.error(f"Camera {camera_id} not found in DB.")
            return False

        if not camera_data['is_active']:
            logger.warning(f"Camera {camera_id} is marked inactive.")
            return False

        source = camera_data['source']
        manager = CameraManager(source, camera_id)
        manager.start()
        self.active_managers[camera_id] = manager
        return True

    def stop_camera(self, camera_id: int):
        if camera_id in self.active_managers:
            self.active_managers[camera_id].stop()
            del self.active_managers[camera_id]

    def stop_all(self):
        for cid in list(self.active_managers.keys()):
            self.stop_camera(cid)

    def get_frame(self, camera_id: int) -> Optional[np.ndarray]:
        if camera_id not in self.active_managers:
            return None
        return self.active_managers[camera_id].read()

    def get_all_cameras(self) -> List[Dict[str, Any]]:
        return self.repo.get_all_cameras()

    def add_camera(self, name: str, source: str, location: str = "", model_name: str = "ppe.pt") -> bool:
        return self.repo.add_camera(name, source, location, model_name)

    def delete_camera(self, camera_id: int) -> bool:
        self.stop_camera(camera_id)
        return self.repo.delete_camera(camera_id)
