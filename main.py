from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests

from db import SessionLocal, engine, Base
from models import RestaurantDB

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to my API"}

@app.get("/suggestion")
def get_weather_suggestion():
    # Chicago coordinates as an example
    latitude = 41.87
    longitude = -87.62

    # Call Open-Meteo's weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()

    temp_c = weather_data["current_weather"]["temperature"]
    condition_code = weather_data["current_weather"]["weathercode"]

    # Smart suggestion based on weather
    if temp_c > 25:
        suggestion = "It's hot outside — stay hydrated or go swimming!"
    elif temp_c > 15:
        suggestion = "Perfect weather for a walk or jog!"
    else:
        suggestion = "It’s chilly — maybe stay in and drink something warm."

    return {
        "temperature": f"{temp_c}°C",
        "suggestion": suggestion
    }

# ---------- Database: Setup ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Pydantic Model ----------
class Restaurant(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True

# ---------- Restaurant Routes ----------
@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(RestaurantDB).all()

@app.post("/restaurants", response_model=Restaurant)
def add_restaurant(restaurant: Restaurant, db: Session = Depends(get_db)):
    db_restaurant = RestaurantDB(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.delete("/restaurants/{restaurant_id}", response_model=Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantDB).filter(RestaurantDB.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(restaurant)
    db.commit()
    return restaurant


