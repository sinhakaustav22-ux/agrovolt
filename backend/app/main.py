from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import crop, solar, irrigation, weather, farms

app = FastAPI(
    title="AgroVolt API",
    description="Smart Agrovoltaic Management System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://agrovolt.vercel.app"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crop.router,       prefix="/api/crop",       tags=["Crop Yield"])
app.include_router(solar.router,      prefix="/api/solar",      tags=["Solar Forecast"])
app.include_router(irrigation.router, prefix="/api/irrigation", tags=["Irrigation"])
app.include_router(weather.router,    prefix="/api/weather",    tags=["Weather"])
app.include_router(farms.router,      prefix="/api/farms",      tags=["Farms"])

@app.get("/")
def root():
    return {"message": "AgroVolt API is running ✅", "docs": "/docs"}
