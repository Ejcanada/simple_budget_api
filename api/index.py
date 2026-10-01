from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="World Heritage Sites API",
    description="A REST API containing 20 historical landmarks and sites globally.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Landmark(BaseModel):
    id: int
    title: str
    site_type: str
    established_year: int
    visitor_rating: str
    governing_body: str
    notable_architects: str
    icon: str
    description: str
    country: str
    region: str
    protection_status: str
    annual_visitors: str
    entry_fee: str

# Database
landmarks = [
    {
        "id": 1,
        "title": "Banaue Rice Terraces",
        "site_type": "Cultural Landscape",
        "established_year": 100,
        "visitor_rating": "4.9/5",
        "governing_body": "UNESCO World Heritage",
        "notable_architects": "Ifugao Ancestors",
        "icon": "/images/banaue.jpg",
        "description": "2,000-year-old terraces carved into the mountains of Ifugao in the Philippines.",
        "country": "Philippines",
        "region": "Southeast Asia",
        "protection_status": "Protected National Cultural Treasure",
        "annual_visitors": "120K Visitors",
        "entry_fee": "₱50 PHP"
    },
    {
        "id": 2,
        "title": "Historic City of Vigan",
        "site_type": "Cultural Heritage",
        "established_year": 1572,
        "visitor_rating": "4.8/5",
        "governing_body": "UNESCO World Heritage",
        "notable_architects": "Spanish Colonial Builders",
        "icon": "/images/vigan.jpg",
        "description": "Best-preserved example of a planned Spanish colonial town in Asia.",
        "country": "Philippines",
        "region": "Southeast Asia",
        "protection_status": "Protected Historic Center",
        "annual_visitors": "450K Visitors",
        "entry_fee": "Free"
    },
    {
        "id": 3,
        "title": "Colosseum",
        "site_type": "Ancient Monument",
        "established_year": 80,
        "visitor_rating": "4.9/5",
        "governing_body": "Ministry of Cultural Heritage",
        "notable_architects": "Flavian Dynasty",
        "icon": "/images/colosseum.jpg",
        "description": "An iconic oval amphitheatre in the centre of the city of Rome, Italy.",
        "country": "Italy",
        "region": "Europe",
        "protection_status": "Protected Archeological Site",
        "annual_visitors": "6.0M Visitors",
        "entry_fee": "€16 EUR"
    },
    {
        "id": 4,
        "title": "Machu Picchu",
        "site_type": "Ancient Ruin",
        "established_year": 1450,
        "visitor_rating": "5.0/5",
        "governing_body": "UNESCO World Heritage",
        "notable_architects": "Inca Civilization",
        "icon": "/images/machu.jpg",
        "description": "A 15th-century Inca citadel located in the Eastern Cordillera of southern Peru.",
        "country": "Peru",
        "region": "South America",
        "protection_status": "Protected Historic Sanctuary",
        "annual_visitors": "1.5M Visitors",
        "entry_fee": "$45 USD"
    },
    {
        "id": 5,
        "title": "Taj Mahal",
        "site_type": "Cultural Monument",
        "established_year": 1653,
        "visitor_rating": "4.9/5",
        "governing_body": "Archaeological Survey of India",
        "notable_architects": "Ustad Ahmad Lahori",
        "icon": "/images/taj.jpg",
        "description": "An ivory-white marble mausoleum on the right bank of the river Yamuna.",
        "country": "India",
        "region": "South Asia",
        "protection_status": "Protected Monument",
        "annual_visitors": "6.5M Visitors",
        "entry_fee": "₹1100 INR"
    },
    {
        "id": 6,
        "title": "Great Wall of China",
        "site_type": "Historical Fortification",
        "established_year": -221,
        "visitor_rating": "4.8/5",
        "governing_body": "State Administration of Cultural Heritage",
        "notable_architects": "Ming Dynasty Builders",
        "icon": "/images/greatwall.jpg",
        "description": "A series of fortifications built across the historical northern borders of China.",
        "country": "China",
        "region": "East Asia",
        "protection_status": "Protected Priority National Site",
        "annual_visitors": "10.0M Visitors",
        "entry_fee": "¥40 CNY"
    },
    {
        "id": 7,
        "title": "Pyramids of Giza",
        "site_type": "Ancient Ruin",
        "established_year": -2560,
        "visitor_rating": "4.7/5",
        "governing_body": "Supreme Council of Antiquities",
        "notable_architects": "Ancient Egyptian Builders",
        "icon": "/images/pyramid.jpg",
        "description": "The oldest of the Seven Wonders of the Ancient World, standing near Cairo.",
        "country": "Egypt",
        "region": "North Africa",
        "protection_status": "Protected World Heritage",
        "annual_visitors": "14.0M Visitors",
        "entry_fee": "240 EGP"
    },
    {
        "id": 8,
        "title": "Acropolis of Athens",
        "site_type": "Ancient Citadel",
        "established_year": -447,
        "visitor_rating": "4.8/5",
        "governing_body": "Hellenic Ministry of Culture",
        "notable_architects": "Ictinus and Callicrates",
        "icon": "/images/athens.jpg",
        "description": "An ancient citadel located on a rocky outcrop above the city of Athens.",
        "country": "Greece",
        "region": "Europe",
        "protection_status": "Protected National Site",
        "annual_visitors": "3.0M Visitors",
        "entry_fee": "€20 EUR"
    },
    {
        "id": 9,
        "title": "Angkor Wat",
        "site_type": "Temple Complex",
        "established_year": 1150,
        "visitor_rating": "4.9/5",
        "governing_body": "APSARA National Authority",
        "notable_architects": "Khmer Empire",
        "icon": "/images/angkor.png",
        "description": "The largest religious structure in the world by land area, located in Cambodia.",
        "country": "Cambodia",
        "region": "Southeast Asia",
        "protection_status": "Protected Archaeological Park",
        "annual_visitors": "2.6M Visitors",
        "entry_fee": "$37 USD"
    },
    {
        "id": 10,
        "title": "Chichen Itza",
        "site_type": "Ancient City",
        "established_year": 600,
        "visitor_rating": "4.8/5",
        "governing_body": "INAH Mexico",
        "notable_architects": "Mayan Civilization",
        "icon": "/images/chichen.jpg",
        "description": "A large pre-Columbian city built by the Maya people of the Terminal Classic period.",
        "country": "Mexico",
        "region": "Latin America",
        "protection_status": "Protected Archaeological Zone",
        "annual_visitors": "2.5M Visitors",
        "entry_fee": "$30 USD"
    },
    {
        "id": 11,
        "title": "Petra",
        "site_type": "Historical City",
        "established_year": -312,
        "visitor_rating": "4.9/5",
        "governing_body": "Petra Development and Tourism Authority",
        "notable_architects": "Nabataean Kingdom",
        "icon": "/images/petra.jpg",
        "description": "Famous for its rock-cut architecture and water conduit system in southern Jordan.",
        "country": "Jordan",
        "region": "Middle East",
        "protection_status": "Protected Archaeological Park",
        "annual_visitors": "1.1M Visitors",
        "entry_fee": "50 JOD"
    },
    {
        "id": 12,
        "title": "Statue of Liberty",
        "site_type": "Historical Monument",
        "established_year": 1886,
        "visitor_rating": "4.7/5",
        "governing_body": "National Park Service",
        "notable_architects": "Frédéric-Auguste Bartholdi",
        "icon": "/images/liberty.jpg",
        "description": "A colossal neoclassical sculpture on Liberty Island in New York Harbor.",
        "country": "United States",
        "region": "North America",
        "protection_status": "National Monument",
        "annual_visitors": "4.4M Visitors",
        "entry_fee": "$24 USD"
    },
    {
        "id": 13,
        "title": "Eiffel Tower",
        "site_type": "Historical Monument",
        "established_year": 1889,
        "visitor_rating": "4.8/5",
        "governing_body": "SETE Paris",
        "notable_architects": "Gustave Eiffel",
        "icon": "/images/eiffel.jpg",
        "description": "A wrought-iron lattice tower on the Champ de Mars in Paris, France.",
        "country": "France",
        "region": "Europe",
        "protection_status": "Protected Historic Monument",
        "annual_visitors": "6.2M Visitors",
        "entry_fee": "€26 EUR"
    },
    {
        "id": 14,
        "title": "Fushimi Inari Taisha",
        "site_type": "Shinto Shrine Complex",
        "established_year": 711,
        "visitor_rating": "4.9/5",
        "governing_body": "Shinto Shrine Management",
        "notable_architects": "Hata Clan",
        "icon": "/images/fushimi.jpg",
        "description": "The head shrine of the kami Inari, located in Fushimi-ku, Kyoto, Japan.",
        "country": "Japan",
        "region": "East Asia",
        "protection_status": "Protected Cultural Property",
        "annual_visitors": "3.0M Visitors",
        "entry_fee": "Free"
    },
    {
        "id": 15,
        "title": "Christ the Redeemer",
        "site_type": "Cultural Monument",
        "established_year": 1931,
        "visitor_rating": "4.8/5",
        "governing_body": "ICMBio Brazil",
        "notable_architects": "Paul Landowski",
        "icon": "/images/christ.jpg",
        "description": "An Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil.",
        "country": "Brazil",
        "region": "South America",
        "protection_status": "Protected National Heritage",
        "annual_visitors": "2.0M Visitors",
        "entry_fee": "R$110 BRL"
    },
    {
        "id": 16,
        "title": "Stonehenge",
        "site_type": "Prehistoric Monument",
        "established_year": -3000,
        "visitor_rating": "4.5/5",
        "governing_body": "English Heritage",
        "notable_architects": "Neolithic Builders",
        "icon": "/images/stone.jpg",
        "description": "A prehistoric monument on Salisbury Plain in Wiltshire, England.",
        "country": "United Kingdom",
        "region": "Europe",
        "protection_status": "Protected Scheduled Monument",
        "annual_visitors": "1.6M Visitors",
        "entry_fee": "£23 GBP"
    },
    {
        "id": 17,
        "title": "Alhambra Palace",
        "site_type": "Palace and Fortress",
        "established_year": 1238,
        "visitor_rating": "4.9/5",
        "governing_body": "Patronato de la Alhambra",
        "notable_architects": "Nasrid Dynasty",
        "icon": "/images/alhambra.jpg",
        "description": "A palace and fortress complex located in Granada, Andalusia, Spain.",
        "country": "Spain",
        "region": "Europe",
        "protection_status": "Protected Historic Site",
        "annual_visitors": "2.7M Visitors",
        "entry_fee": "€14 EUR"
    },
    {
        "id": 18,
        "title": "Borobudur Temple",
        "site_type": "Buddhist Temple",
        "established_year": 825,
        "visitor_rating": "4.8/5",
        "governing_body": "Ministry of Education and Culture",
        "notable_architects": "Gunadharma",
        "icon": "/images/boro.jpg",
        "description": "The world's largest Buddhist temple, located in Central Java, Indonesia.",
        "country": "Indonesia",
        "region": "Southeast Asia",
        "protection_status": "Protected National Cultural Property",
        "annual_visitors": "2.1M Visitors",
        "entry_fee": "IDR 375K"
    },
    {
        "id": 19,
        "title": "Sydney Opera House",
        "site_type": "Modern Performing Arts",
        "established_year": 1973,
        "visitor_rating": "4.8/5",
        "governing_body": "Sydney Opera House Trust",
        "notable_architects": "Jørn Utzon",
        "icon": "/images/sydney.jpg",
        "description": "A multi-venue performing arts centre in Sydney Harbour, Australia.",
        "country": "Australia",
        "region": "Oceania",
        "protection_status": "Protected State Heritage",
        "annual_visitors": "10.0M Visitors",
        "entry_fee": "$43 AUD"
    },
    {
        "id": 20,
        "title": "Hagia Sophia",
        "site_type": "Historical Architecture",
        "established_year": 537,
        "visitor_rating": "4.9/5",
        "governing_body": "Ministry of Culture and Tourism",
        "notable_architects": "Isidore of Miletus",
        "icon": "/images/hagia.jpg",
        "description": "A major cultural and historical monument in Istanbul, Turkey.",
        "country": "Turkey",
        "region": "Middle East / Europe",
        "protection_status": "Protected Historical Reserve",
        "annual_visitors": "3.7M Visitors",
        "entry_fee": "€25 EUR"
    }
]

# FIX: Replaced .model_dump() with .dict() to prevent Vercel 500 crashes
validated_landmarks = [Landmark(**landmark).dict() for landmark in landmarks]
landmarks = validated_landmarks

# ==========================================
# API KEY AUTHENTICATION
# ==========================================
API_KEY = "my_secret_landmark_key" 

def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="401 error Invalid, Missing api key."
        )
    return True

# FIX: Added /api to all paths so they align with Vercel's routing rules

# HOME (Public)
@app.get("/api")
def home():
    return {
        "message": "Welcome to the World Heritage Sites API!",
        "count": len(landmarks),
        "endpoints": [
            "/api/health",
            "/api/landmarks",
            "/api/landmarks/{id}",
            "/api/landmarks/search"
        ]
    }

# HEALTH CHECK (Public)
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "World Heritage Sites API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# GET ALL LANDMARKS (Protected)
@app.get("/api/landmarks", response_model=dict, dependencies=[Depends(verify_api_key)])
def get_landmarks():
    return {
        "count": len(landmarks),
        "landmarks": landmarks
    }

# SEARCH LANDMARKS (Protected)
@app.get("/api/landmarks/search", response_model=dict, dependencies=[Depends(verify_api_key)])
def search_landmarks(q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    
    for item in landmarks:
        searchable_text = (
            f"{item['title']} "
            f"{item['site_type']} "
            f"{item['country']} "
            f"{item['region']} "
            f"{item['governing_body']} "
            f"{item['established_year']} "
            f"{item['notable_architects']} "
            f"{item['protection_status']} "
            f"{item['description']}"
        ).lower()

        if q in searchable_text:
            results.append(item)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# GET ONE LANDMARK (Protected)
@app.get("/api/landmarks/{landmark_id}", response_model=Landmark, dependencies=[Depends(verify_api_key)])
def get_landmark(landmark_id: int):
    for item in landmarks:
        if item["id"] == landmark_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Landmark not found."
    )
