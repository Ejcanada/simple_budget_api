from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Budget Matcher API",
    description="A REST API containing global travel destinations and budget calculations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Destination(BaseModel):
    id: int
    name: str
    country: str
    tag: str
    daily_cost: float
    image: str
    description: str
    best_time_to_visit: str

# Database of destinations for the Budget Matcher
destinations = [
    {
        "id": 1,
        "name": "Chiang Mai",
        "country": "Thailand",
        "tag": "Nature",
        "daily_cost": 42.0,
        "image": "/images/chiangmai.jpg",
        "description": "A haven for digital nomads and nature lovers in mountainous Northern Thailand.",
        "best_time_to_visit": "November to February"
    },
    {
        "id": 2,
        "name": "Kyoto",
        "country": "Japan",
        "tag": "Heritage",
        "daily_cost": 95.0,
        "image": "/images/kyoto.jpg",
        "description": "Famous for its classical Buddhist temples, gardens, imperial palaces, and traditional wooden houses.",
        "best_time_to_visit": "March to May (Cherry Blossoms)"
    },
    {
        "id": 3,
        "name": "Hanoi",
        "country": "Vietnam",
        "tag": "City",
        "daily_cost": 35.0,
        "image": "/images/hanoi.jpg",
        "description": "Known for its centuries-old architecture and a rich culture with Southeast Asian, Chinese and French influences.",
        "best_time_to_visit": "February to April"
    },
    {
        "id": 4,
        "name": "Palawan",
        "country": "Philippines",
        "tag": "Nature",
        "daily_cost": 45.0,
        "image": "/images/palawan.jpg",
        "description": "An archipelagic province known for its crystal-clear waters, limestone cliffs, and rich marine biodiversity.",
        "best_time_to_visit": "October to May"
    },
    {
        "id": 5,
        "name": "Bali",
        "country": "Indonesia",
        "tag": "Beach",
        "daily_cost": 60.0,
        "image": "/images/bali.jpg",
        "description": "An Indonesian island known for its forested volcanic mountains, iconic rice paddies, beaches and coral reefs.",
        "best_time_to_visit": "April to October"
    },
    {
        "id": 6,
        "name": "Paris",
        "country": "France",
        "tag": "Culture",
        "daily_cost": 150.0,
        "image": "/images/paris.jpg",
        "description": "France's capital, a major European city and global center for art, fashion, gastronomy and culture.",
        "best_time_to_visit": "June to August"
    }
]

# Using .dict() instead of .model_dump() to prevent 500 errors on Vercel's environment
validated_destinations = [Destination(**dest).dict() for dest in destinations]
destinations = validated_destinations

# ==========================================
# API KEY AUTHENTICATION
# ==========================================
API_KEY = "my_secret_budget_key"

def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="401 error Invalid, Missing api key."
        )
    return True

# HOME (Public)
@app.get("/")
def home():
    return {
        "message": "Welcome to the Budget Matcher API!",
        "count": len(destinations),
        "endpoints": [
            "/health",
            "/destinations",
            "/destinations/{id}",
            "/api/match"
        ]
    }

# HEALTH CHECK (Public)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Budget Matcher API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# GET ALL DESTINATIONS (Protected)
@app.get("/destinations", response_model=dict, dependencies=[Depends(verify_api_key)])
def get_destinations():
    return {
        "count": len(destinations),
        "destinations": destinations
    }

# MATCH BUDGET (Protected - Replaces the old search endpoint)
@app.get("/api/match", response_model=dict, dependencies=[Depends(verify_api_key)])
def match_budget(budget: float = Query(...), duration: int = Query(...)):
    matches = []
    
    for dest in destinations:
        trip_total = dest["daily_cost"] * duration
        spare = budget - trip_total
        
        if spare >= 0:
            # We copy the dictionary so we can inject calculated totals without altering the original database
            match_data = dest.copy()
            match_data["trip_total"] = trip_total
            match_data["spare"] = spare
            matches.append(match_data)

    return {
        "budget": budget,
        "duration": duration,
        "count": len(matches),
        "matches": matches
    }

# GET ONE DESTINATION (Protected)
@app.get("/destinations/{dest_id}", response_model=Destination, dependencies=[Depends(verify_api_key)])
def get_destination(dest_id: int):
    for item in destinations:
        if item["id"] == dest_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Destination not found."
    )
