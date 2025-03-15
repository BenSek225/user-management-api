# fastapi_version/main.py
from fastapi import FastAPI
from database import init_db
from routes import register_routes

app = FastAPI(title="User Management API - FastAPI")
init_db()
register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)