import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret")

    SQLALCHEMY_DATABASE_URI = "sqlite:///billing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MINIO_ENDPOINT   = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    MINIO_SECURE     = os.getenv("MINIO_SECURE", "False") == "True"


    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

    STORAGE_QUOTA_BYTES = 50 * 1024 * 1024

    BLOCKED_EXTENSIONS = {
        ".exe", ".bat", ".sh", ".cmd", ".ps1",
        ".php", ".py", ".rb", ".js", ".jar",
        ".msi", ".dll", ".vbs", ".scr"
    }

    ALLOWED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".gif", ".webp",  # images
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",  # documents
        ".txt", ".csv", ".json", ".xml",            # text/data
        ".mp4", ".mp3", ".zip", ".tar", ".gz"       # media/archives
    }