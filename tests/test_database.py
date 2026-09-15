import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import init_database
from database.camera_repository import CameraRepository

def test_db():
    print("Testing DB connection and initialization...")
    init_database()
    
    repo = CameraRepository()
    cameras = repo.get_all_cameras()
    print(f"Total cameras in DB: {len(cameras)}")
    for c in cameras:
        print(f" - {c['id']}: {c['name']} (Source: {c['source']})")
    
    print("DB Test Completed Successfully.")

if __name__ == "__main__":
    test_db()
