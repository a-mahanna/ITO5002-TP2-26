"""
main.py — Livability.AI FastAPI Backend
Serves suburb data to Ali's Vue.js frontend.

Setup:
  pip install -r requirements.txt

Run:
  uvicorn main:app --reload --port 8000

API Docs:
  http://localhost:8000/docs
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
from pathlib import Path
from recommender import SuburbRecommender

app = FastAPI(
    title="Livability.AI API",
    description="Melbourne suburb livability data for renters",
    version="1.0.0"
)

# Allow Ali's Vue.js frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data + recommender loaded on startup
DATA_PATH = Path(__file__).parent / "data" / "suburbs.json"
SUBURB_DATA = {}
recommender = None


@app.on_event("startup")
def load_data():
    global SUBURB_DATA, recommender
    if not DATA_PATH.exists():
        print("ERROR: data/suburbs.json not found!")
        return
    with open(DATA_PATH) as f:
        SUBURB_DATA = json.load(f)
    recommender = SuburbRecommender(SUBURB_DATA["suburbs"])
    print(f"Loaded {SUBURB_DATA['suburb_count']} suburbs")


# =============================================
# VERSION 1 ENDPOINTS (Suburb Lookup)
# =============================================

@app.get("/")
def root():
    return {
        "name": "Livability.AI API",
        "version": "1.0.0",
        "suburbs_loaded": SUBURB_DATA.get("suburb_count", 0)
    }


@app.get("/api/v1/suburbs")
def list_suburbs():
    """List all suburb names (for search/autocomplete)."""
    suburbs = SUBURB_DATA.get("suburbs", [])
    return {
        "count": len(suburbs),
        "suburbs": sorted([s["name"] for s in suburbs])
    }


@app.get("/api/v1/suburbs/all")
def all_suburbs_data():
    """Return full data for all suburbs (for map rendering)."""
    return SUBURB_DATA


@app.get("/api/v1/suburbs/{suburb_name}")
def get_suburb(suburb_name: str):
    """Lookup a specific suburb — returns all metrics + Melbourne averages."""
    suburbs = SUBURB_DATA.get("suburbs", [])

    # Exact match (case-insensitive)
    match = next((s for s in suburbs if s["name"].lower() == suburb_name.lower()), None)

    # Partial match fallback
    if not match:
        matches = [s for s in suburbs if suburb_name.lower() in s["name"].lower()]
        if len(matches) == 1:
            match = matches[0]
        elif len(matches) > 1:
            return {"error": "Multiple matches", "matches": [s["name"] for s in matches]}
        else:
            raise HTTPException(status_code=404, detail=f"Suburb '{suburb_name}' not found")

    return {
        "suburb": match,
        "melbourne_averages": SUBURB_DATA.get("melbourne_averages", {})
    }


@app.get("/api/v1/search")
def search(q: str = Query(..., min_length=1)):
    """Search suburbs by name (partial match)."""
    suburbs = SUBURB_DATA.get("suburbs", [])
    matches = [s for s in suburbs if q.lower() in s["name"].lower()]
    return {
        "query": q,
        "count": len(matches),
        "results": [{
            "name": s["name"],
            "rent_2bed": s["rent"].get("2bed_flat"),
            "total_offences": s["crime"].get("total_offences"),
            "offence_rate_1000": s["crime"].get("offence_rate_1000"),
            "transport_stops": s["transport"].get("total_stops"),
            "scores": s["scores"],
            "distance_to_cbd_km": s.get("distance_to_cbd_km"),
        } for s in matches]
    }


@app.get("/api/v1/averages")
def get_averages():
    """Melbourne-wide averages for all metrics."""
    return SUBURB_DATA.get("melbourne_averages", {})


@app.get("/api/v1/compare")
def compare_suburbs(
    suburbs: str = Query(..., description="Comma-separated suburb names (max 3)")
):
    """Compare up to 3 suburbs side by side."""
    names = [n.strip() for n in suburbs.split(",")][:3]
    all_suburbs = SUBURB_DATA.get("suburbs", [])
    averages = SUBURB_DATA.get("melbourne_averages", {})

    results = []
    for name in names:
        match = next((s for s in all_suburbs if s["name"].lower() == name.lower()), None)
        if match:
            results.append(match)
        else:
            # Try partial match
            partial = [s for s in all_suburbs if name.lower() in s["name"].lower()]
            if partial:
                results.append(partial[0])

    return {
        "count": len(results),
        "suburbs": results,
        "melbourne_averages": averages
    }


# =============================================
# VERSION 2 ENDPOINTS (AI Features)
# =============================================

@app.get("/api/v2/explain/{suburb_name}")
def explain_suburb(
    suburb_name: str,
    budget: float = Query(None, description="Weekly rent budget ($)")
):
    """Explainability Engine — plain-English explanation of suburb metrics."""
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not ready")

    result = recommender.explain(suburb_name, budget)
    if result is None:
        raise HTTPException(status_code=404, detail=f"'{suburb_name}' not found")
    return result


@app.get("/api/v2/similar/{suburb_name}")
def find_similar(
    suburb_name: str,
    n: int = Query(5, ge=1, le=20, description="Number of similar suburbs")
):
    """Similarity Engine — find suburbs with comparable metric profiles."""
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not ready")

    result = recommender.find_similar(suburb_name, n)
    if result is None:
        raise HTTPException(status_code=404, detail=f"'{suburb_name}' not found")
    return result


@app.get("/api/v2/recommend")
def recommend(
    budget: float = Query(..., description="Max weekly rent ($)"),
    property_type: str = Query("2bed_flat",
        description="1bed_flat, 2bed_flat, 3bed_flat, 2bed_house, 3bed_house"),
    safety_weight: float = Query(0.5, ge=0, le=1, description="Safety importance (0-1)"),
    transport_weight: float = Query(0.5, ge=0, le=1, description="Transport importance (0-1)"),
    n: int = Query(10, ge=1, le=50, description="Number of results")
):
    """Recommend suburbs matching user preferences."""
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not ready")

    return recommender.recommend(
        budget=budget,
        property_type=property_type,
        safety_weight=safety_weight,
        transport_weight=transport_weight,
        n=n
    )


@app.get("/api/v2/clusters")
def get_clusters():
    """Suburb clusters from k-means analysis."""
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not ready")
    return recommender.get_clusters()
