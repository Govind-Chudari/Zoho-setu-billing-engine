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