# UI Components
from .theme import custom_theme, custom_css
from .dashboard import create_dashboard_tab
from .camera_page import create_camera_tab
from .alerts_page import create_alerts_tab
from .analytics_page import create_analytics_tab
from .settings_page import create_settings_tab

__all__ = [
    "custom_theme",
    "custom_css",
    "create_dashboard_tab",
    "create_camera_tab",
    "create_alerts_tab",
    "create_analytics_tab",
    "create_settings_tab"
]
