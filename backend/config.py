import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'smart-resume-secret-key-2024-change-in-prod')
    # Use /tmp on Vercel/serverless (writable), fallback to local path
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'pdf'}
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    # Session config
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_sessions'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
