# fastapi_version/routes.py
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserCreate, UserOut, UserLogin  # Ajoute UserLogin
from auth import create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(400, "Utilisateur existe déjà")
    user = User(username=user_in.username, email=user_in.email)
    user.set_password(user_in.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):  # Change UserCreate en UserLogin
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not user.check_password(user_in.password):
        raise HTTPException(401, "Identifiants invalides")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    return user

@router.put("/profile", response_model=UserOut)
def update_profile(user_in: UserCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    user.email = user_in.email
    user.set_password(user_in.password)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/profile")
def delete_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    db.delete(user)
    db.commit()
    return {"message": "Compte supprimé"}

def register_routes(app):
    app.include_router(router)