from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2AuthorizationCodeBearer
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
import requests

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db)):
    # Here, you should check session data or cookie authentication
    # For now, let's assume the user is stored in the database
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}

@router.get("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.get("/google-login")
def google_login():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth"
               f"?response_type=code&client_id={GOOGLE_CLIENT_ID}"
               f"&redirect_uri=http://localhost:8000/auth/google-callback"
               f"&scope=email%20profile"
    }

@router.get("/google-callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/auth/google-callback",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_info = response.json()

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {token_info.get('access_token')}"}
    user_info = requests.get(user_info_url, headers=headers).json()

    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        user = User(name=user_info["name"], email=user_info["email"])
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"message": "Google login successful", "user": user}
