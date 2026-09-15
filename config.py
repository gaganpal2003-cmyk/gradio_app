import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Database Settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Gagan@123")
DB_NAME = os.getenv("DB_NAME", "bothera_ai_db")

# Directories
MODELS_DIR = BASE_DIR / "Models"
if not MODELS_DIR.exists():
    MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR = BASE_DIR / "data"
ALERTS_DIR = DATA_DIR / "alerts"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
LOGS_DIR = DATA_DIR / "logs"

for directory in [DATA_DIR, ALERTS_DIR, SNAPSHOTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default Model Settings
DEFAULT_MODEL_NAME = "ppe.pt"
DEFAULT_MODEL_PATH = str(MODELS_DIR / DEFAULT_MODEL_NAME)
CONF_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.35"))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", "0.45"))

# Alert Settings
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "10"))
VIOLATION_CLASSES = ["no_helmet", "no_vest", "no_safty_shoes", "no_safety_shoes"]
COMPLIANT_CLASSES = ["helmet", "vest", "safty_shoes", "safety_shoes"]

# Server Settings
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "7860"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
