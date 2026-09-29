from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard Python dictionary (No Pydantic to prevent 500 errors)
destinations = [
    {"id": 1, "name": "Chiang Mai", "country": "Thailand", "tag": "Nature", "daily_cost": 42.0, "image": "/images/chiangmai.jpg"},
    {"id": 2, "name": "Kyoto", "country": "Japan", "tag": "Heritage", "daily_cost": 95.0, "image": "/images/kyoto.jpg"},
    {"id": 3, "name": "Hanoi", "country": "Vietnam", "tag": "City", "daily_cost": 35.0, "image": "/images/hanoi.jpg"},
    {"id": 4, "name": "Palawan", "country": "Philippines", "tag": "Nature", "daily_cost": 45.0, "image": "/images/palawan.jpg"},
    {"id": 5, "name": "Bali", "country": "Indonesia", "tag": "Beach", "daily_cost": 60.0, "image": "/images/bali.jpg"},
    {"id": 6, "name": "Paris", "country": "France", "tag": "Culture", "daily_cost": 150.0, "image": "/images/paris.jpg"}
]

API_KEY = "my_secret_budget_key"

def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Missing or Invalid API Key")
    return True

# Changed root to /api to stop Vercel from hijacking the home page
@app.get("/api")
def home():
    return {"message": "API is online and correctly routed!"}

@app.get("/api/match", dependencies=[Depends(verify_api_key)])
def match_budget(budget: float = Query(...), duration: int = Query(...)):
    matches = []
    
    for dest in destinations:
        trip_total = dest["daily_cost"] * duration
        spare = budget - trip_total
        
        if spare >= 0:
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
