from datetime import datetime
from typing import Optional
import time

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Employee, Property, PropertyImage, Developer, SiteSetting

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")

# Generated once when the app starts – changes on every deploy
CACHE_VERSION = str(int(time.time()))

# Default fallback values if DB settings are missing
SETTING_DEFAULTS = {
    "hero_image_url":        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1800&q=80",
    "about_hero_image_url":  "https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=1800&q=80",
    "about_story_image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=900&q=80",
}


def get_settings(db: Session) -> dict:
    """Load all site_settings rows into a plain dict, falling back to defaults."""
    rows = db.query(SiteSetting).all()
    result = dict(SETTING_DEFAULTS)
    for row in rows:
        if row.value:
            result[row.key] = row.value
    return result


# ---------------------------------------------------------------------------
# Home  /
# ---------------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    featured = (
        db.query(Property)
        .filter(Property.is_featured == True, Property.is_active == True)
        .order_by(Property.created_at.desc())
        .limit(6)
        .all()
    )

    total      = db.query(Property).filter(Property.is_active == True).count()
    for_sale   = db.query(Property).filter(Property.is_active == True, Property.listing_type == "sale").count()
    for_rent   = db.query(Property).filter(Property.is_active == True, Property.listing_type == "rent").count()
    emirates   = db.query(Property.emirate).filter(Property.is_active == True).distinct().count()

    devs = (
        db.query(Developer)
        .filter(Developer.is_active == True)
        .order_by(Developer.sort_order, Developer.id)
        .all()
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "featured_properties": featured,
        "developers": devs,
        "settings": get_settings(db),
        "stats": {
            "total":    total,
            "for_sale": for_sale,
            "for_rent": for_rent,
            "emirates": emirates,
        },
        "year": datetime.now().year,
        "cache_version": CACHE_VERSION,
    })


# ---------------------------------------------------------------------------
# Properties  /properties
# ---------------------------------------------------------------------------
@router.get("/properties", response_class=HTMLResponse)
def properties_page(
    request: Request,
    listing_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Property).filter(Property.is_active == True)

    if listing_type in ("sale", "rent"):
        query = query.filter(Property.listing_type == listing_type)

    props = query.order_by(Property.created_at.desc()).all()

    return templates.TemplateResponse("properties.html", {
        "request":       request,
        "properties":    props,
        "active_filter": listing_type,
        "year":          datetime.now().year,
        "cache_version": CACHE_VERSION,
    })


# ---------------------------------------------------------------------------
# Property detail  /properties/{id}
# ---------------------------------------------------------------------------
@router.get("/properties/{property_id}", response_class=HTMLResponse)
def property_detail(property_id: int, request: Request, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.is_active == True,
    ).first()

    if not prop:
        from fastapi.responses import HTMLResponse
        return HTMLResponse(status_code=404, content="Property not found")

    images = (
        db.query(PropertyImage)
        .filter(PropertyImage.property_id == property_id)
        .order_by(PropertyImage.sort_order)
        .all()
    )

    # Fall back to the primary image_filename if no gallery images exist
    if not images and prop.image_filename:
        images = [type('obj', (object,), {'image_url': prop.image_filename})()]

    return templates.TemplateResponse("property_detail.html", {
        "request":  request,
        "prop":     prop,
        "images":   images,
        "year":     datetime.now().year,
        "cache_version": CACHE_VERSION,
    })


# ---------------------------------------------------------------------------
# About  /about
# ---------------------------------------------------------------------------
@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).order_by(Employee.id).all()

    return templates.TemplateResponse("about.html", {
        "request":   request,
        "employees": employees,
        "settings":  get_settings(db),
        "year":      datetime.now().year,
        "cache_version": CACHE_VERSION,
    })


# ---------------------------------------------------------------------------
# Contact  /contactus
# ---------------------------------------------------------------------------
@router.get("/contactus", response_class=HTMLResponse)
def contact_page(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).order_by(Employee.id).all()

    return templates.TemplateResponse("contactus.html", {
        "request":   request,
        "employees": employees,
        "year":      datetime.now().year,
        "cache_version": CACHE_VERSION,
    })