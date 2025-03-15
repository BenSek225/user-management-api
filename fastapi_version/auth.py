# fastapi_version/auth.py
import jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config import Config
import bcrypt

SECRET_KEY = Config.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hachage."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Récupère l’utilisateur à partir du token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(401, "Token invalide")
        return {"sub": username}
    except jwt.PyJWTError:
        raise HTTPException(401, "Token invalide")