# main.py
from fastapi import FastAPI
from auth import router as auth_router
from user_routes import router as user_router
from weather import router as weather_router
from database import engine, Base
import models

app = FastAPI(title="Authentication API")

Base.metadata.create_all(bind=engine)

# Include Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Authentication API"}

# Run with: uvicorn main:app --reload
