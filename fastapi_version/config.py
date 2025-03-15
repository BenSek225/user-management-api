# fastapi_version/config.py
import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Ben_Sek_PostgreSQL@localhost:5432/users_db")
    SECRET_KEY = os.getenv("SECRET_KEY", "votre_cle_secrete")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "votre_jwt_secrete")