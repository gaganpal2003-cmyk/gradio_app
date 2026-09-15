import pymysql
import pymysql.cursors
from contextlib import contextmanager
import config
from app_utils.logger import logger

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.host = config.DB_HOST
            cls._instance.port = config.DB_PORT
            cls._instance.user = config.DB_USER
            cls._instance.password = config.DB_PASSWORD
            cls._instance.db_name = config.DB_NAME
        return cls._instance

    @contextmanager
    def get_connection(self, use_dict_cursor=True, connect_to_db=True):
        conn = None
        try:
            kwargs = {
                "host": self.host,
                "port": self.port,
                "user": self.user,
                "password": self.password,
                "autocommit": True,
            }
            if connect_to_db:
                kwargs["database"] = self.db_name

            if use_dict_cursor:
                kwargs["cursorclass"] = pymysql.cursors.DictCursor
            else:
                kwargs["cursorclass"] = pymysql.cursors.Cursor

            conn = pymysql.connect(**kwargs)
            yield conn
        except pymysql.MySQLError as e:
            logger.error(f"Database connection error: {e}")
            raise e
        finally:
            if conn and conn.open:
                conn.close()

def get_db_connection():
    return DatabaseConnection()

def init_database():
    db = get_db_connection()
    logger.info("Initializing database...")

    # 1. Create database if not exists
    try:
        with db.get_connection(connect_to_db=False) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db.db_name}")
                logger.info(f"Database {db.db_name} verified/created.")
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        return

    # 2. Create Tables
    queries = [
        """
        CREATE TABLE IF NOT EXISTS cameras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            source VARCHAR(255) NOT NULL,
            location VARCHAR(150) DEFAULT 'Main Facility',
            is_active BOOLEAN DEFAULT TRUE,
            model_name VARCHAR(100) DEFAULT 'ppe.pt',
            conf_threshold FLOAT DEFAULT 0.35,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            camera_id INT,
            camera_name VARCHAR(100),
            violation_type VARCHAR(100) NOT NULL,
            severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'HIGH',
            confidence FLOAT DEFAULT 0.0,
            track_id INT DEFAULT NULL,
            snapshot_path VARCHAR(255),
            status ENUM('UNRESOLVED', 'ACKNOWLEDGED', 'RESOLVED') DEFAULT 'UNRESOLVED',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (camera_id) REFERENCES cameras(id) ON DELETE SET NULL,
            INDEX idx_timestamp (timestamp),
            INDEX idx_violation (violation_type)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS detections (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            camera_id INT,
            class_name VARCHAR(100) NOT NULL,
            confidence FLOAT NOT NULL,
            bbox VARCHAR(100) NOT NULL,
            track_id INT DEFAULT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_cam_time (camera_id, timestamp)
        )
        """
    ]

    try:
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                for q in queries:
                    cursor.execute(q)
                logger.info("Database schema initialized successfully.")

                # 3. Seed default camera if none exist
                cursor.execute("SELECT COUNT(*) as count FROM cameras")
                if cursor.fetchone()['count'] == 0:
                    cursor.execute(
                        "INSERT INTO cameras (name, source, location, model_name, conf_threshold) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        ("Default Webcam", "0", "Main Entrance", "ppe.pt", 0.35)
                    )
                    logger.info("Seeded default webcam into database.")
    except Exception as e:
        logger.error(f"Error initializing schema: {e}")
