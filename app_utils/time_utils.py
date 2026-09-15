from datetime import datetime, timedelta
from typing import Optional

def get_current_timestamp() -> str:
    """Returns ISO format timestamp string for database storage."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_datetime(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)

def format_time_ago(dt: datetime) -> str:
    """Returns human-friendly relative time e.g., '2 minutes ago'."""
    if dt is None:
        return "N/A"
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return dt

    diff = datetime.now() - dt
    seconds = int(diff.total_seconds())

    if seconds < 5:
        return "just now"
    elif seconds < 60:
        return f"{seconds}s ago"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    else:
        days = seconds // 86400
        return f"{days}d ago"
