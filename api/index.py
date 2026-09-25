from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Budget Matcher API",
    description="A REST API calculating travel destination affordability based on budget and duration.",
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
    name: str
    country: str
    tag: str
    daily_cost: float
    image: str

# Mock database of global destinations matching your Figma design
destinations_db = [
    {
        "name": "Chiang Mai", 
        "country": "Thailand", 
        "tag": "Nature", 
        "daily_cost": 42.0, 
        "image": "/images/chiangmai.jpg"  # Make sure this matches your exact filename
    },
    {
        "name": "Kyoto", 
        "country": "Japan", 
        "tag": "Heritage", 
        "daily_cost": 95.0, 
        "image": "/images/kyoto.jpg"
    },
    {
        "name": "Hanoi", 
        "country": "Vietnam", 
        "tag": "City", 
        "daily_cost": 35.0, 
        "image": "/images/hanoi.jpg"
    },
    {
        "name": "Palawan", 
        "country": "Philippines", 
        "tag": "Nature", 
        "daily_cost": 45.0, 
        "image": "/images/palawan.jpg"
    },
    {
        "name": "Bali", 
        "country": "Indonesia", 
        "tag": "Beach", 
        "daily_cost": 60.0, 
        "image": "/images/bali.jpg"
    },
    {
        "name": "Paris", 
        "country": "France", 
        "tag": "Culture", 
        "daily_cost": 150.0, 
        "image": "/images/paris.jpg"
    }
]

validated_destinations = [Destination(**dest).model_dump() for dest in destinations_db]

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
@app.get("/api")
def home():
    return {
        "message": "Welcome to the Budget Matcher API!",
        "count": len(validated_destinations),
        "endpoints": [
            "/api/health",
            "/api/match"
        ]
    }

# HEALTH CHECK (Public)
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Budget Matcher API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# MATCH BUDGET (Protected)
@app.get("/api/match", response_model=dict, dependencies=[Depends(verify_api_key)])
def match_budget(budget: float = Query(...), duration: int = Query(...)):
    matches = []
    
    for dest in validated_destinations:
        trip_total = dest["daily_cost"] * duration
        spare = budget - trip_total
        
        if spare >= 0:
            matches.append({
                "name": dest["name"],
                "country": dest["country"],
                "tag": dest["tag"],
                "daily_cost": dest["daily_cost"],
                "trip_total": trip_total,
                "spare": spare,
                "image": dest["image"]
            })
            
    return {
        "duration": duration,
        "count": len(matches),
        "matches": matches
    }
