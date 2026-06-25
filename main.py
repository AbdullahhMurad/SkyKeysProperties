# SKP BACKEND FIRST


from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import Base, engine
from app.routers import employees, properties, pages

# ---------------------------------------------------------------------------
# Ensure required directories exist before FastAPI tries to mount them
# ---------------------------------------------------------------------------
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Create all tables on startup (mirrors the SQL schema)
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SkyKeysProperties",
    description="Luxury real estate platform for Dubai, Abu Dhabi, and Sharjah.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Static files & templates (used by Jinja2 page routes added later)
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------
app.include_router(employees.router, prefix="/api")
app.include_router(properties.router, prefix="/api")
app.include_router(pages.router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
