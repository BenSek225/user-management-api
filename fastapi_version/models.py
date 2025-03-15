# fastapi_version/models.py
from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, UTC  # Ajoute UTC
import bcrypt

# Modèle SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(String(20), default=lambda: datetime.now(UTC).strftime("%Y-%m-%d %H:%M"))

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Modèles Pydantic
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):  # Nouveau modèle pour la connexion
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)  # Nouvelle méthode