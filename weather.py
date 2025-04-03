from fastapi import APIRouter, Depends
import requests
from auth import get_current_user

router = APIRouter()

def fetch_weather():
    response = requests.get("https://api.data.gov.sg/v1/environment/air-temperature")
    return response.json()

@router.get("/")
def get_weather(user: dict = Depends(get_current_user)):
    return fetch_weather()
