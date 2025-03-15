# flask_version/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "votre_cle_secrete")
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "votre_jwt_secrete")