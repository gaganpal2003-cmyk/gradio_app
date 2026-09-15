from typing import Dict, Any, List
from database.detection_repository import DetectionRepository
from database.alert_repository import AlertRepository
from database.camera_repository import CameraRepository
import config

class StatisticsService:
    def __init__(self):
        self.det_repo = DetectionRepository()
        self.alert_repo = AlertRepository()
        self.cam_repo = CameraRepository()

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        alerts_stat = self.alert_repo.get_alert_stats()
        cameras = self.cam_repo.get_all_cameras(active_only=True)
        active_cams_count = len(cameras)
        
        # Calculate Compliance %
        det_counts = self.det_repo.get_detection_counts_by_class(hours=24)
        total_violations = 0
        total_compliant = 0
        
        for cls_name, count in det_counts.items():
            if cls_name.lower() in config.VIOLATION_CLASSES or "no_" in cls_name.lower():
                total_violations += count
            elif cls_name.lower() in config.COMPLIANT_CLASSES:
                total_compliant += count
                
        total_checks = total_violations + total_compliant
        compliance_pct = 100.0
        if total_checks > 0:
            compliance_pct = (total_compliant / total_checks) * 100.0

        return {
            "active_cameras": active_cams_count,
            "today_alerts": alerts_stat["today"],
            "critical_alerts": alerts_stat["unresolved_critical"],
            "compliance_pct": round(compliance_pct, 1)
        }

    def get_hourly_trends(self, hours: int = 24) -> List[Dict[str, Any]]:
        return self.det_repo.get_hourly_trends(hours=hours)

    def get_violation_breakdown(self, hours: int = 24) -> Dict[str, int]:
        det_counts = self.det_repo.get_detection_counts_by_class(hours=hours)
        violation_counts = {}
        for cls_name, count in det_counts.items():
            if cls_name.lower() in config.VIOLATION_CLASSES or "no_" in cls_name.lower():
                violation_counts[cls_name] = count
        return violation_counts
