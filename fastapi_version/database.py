# fastapi_version/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from config import Config

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # Toujours valide, mais pour supprimer l'avertissement :

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)