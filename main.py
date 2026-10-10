"""
AstroCast Main Application Server
FastAPI web application serving the celestial seeing forecast engine.
"""

import os
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.model import seeing_engine
from app.astronomical import calculate_moon_phase, get_tonight_celestial_targets, calculate_observation_window
from app.weather_service import fetch_weather_features, PRESET_LOCATIONS

app = FastAPI(
    title="AstroCast",
    description="Offline-First Tabular Celestial Seeing & Stargazing Predictor",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/")
async def index_page(request: Request):
    """Renders the sleek AstroCast homepage."""
    moon = calculate_moon_phase()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "moon": moon,
            "presets": PRESET_LOCATIONS
        }
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Render deployment."""
    return {"status": "healthy", "service": "AstroCast", "version": "1.0.0"}

@app.get("/api/presets")
async def list_presets():
    """Returns available dark sky and observation presets."""
    return PRESET_LOCATIONS

@app.get("/api/forecast")
async def get_forecast(
    lat: float = Query(default=32.78, description="Latitude"),
    lon: float = Query(default=78.96, description="Longitude"),
    location_name: str = Query(default="Hanle Dark Sky Reserve (Ladakh)", description="Human-readable location")
):
    """
    Main forecast prediction pipeline:
    1. Computes real-time lunar cycle
    2. Fetches microclimate parameters (or offline fallback)
    3. Runs tabular AI seeing & transparency model
    4. Computes celestial observation window & naked-eye targets
    """
    # 1. Astronomical computations
    moon = calculate_moon_phase()
    targets = get_tonight_celestial_targets()

    # 2. Weather & microclimate features
    weather = fetch_weather_features(lat, lon)
    features = {
        **weather,
        "moon_illumination": moon["illumination_percent"]
    }

    # 3. Open-source tabular AI prediction
    prediction = seeing_engine.predict(features)

    # 4. Observation window
    window = calculate_observation_window(
        prediction["seeing_score"],
        moon["illumination_percent"]
    )

    return JSONResponse({
        "location": {
            "name": location_name,
            "lat": lat,
            "lon": lon
        },
        "moon": moon,
        "weather": weather,
        "prediction": prediction,
        "window": window,
        "targets": targets
    })

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
