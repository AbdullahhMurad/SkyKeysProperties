from typing import List, Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Property
from app.schemas.schemas import PropertyCreate, PropertyRead

router = APIRouter(prefix="/properties", tags=["Properties"])


# ---------------------------------------------------------------------------
# GET /properties  –  return all active properties
#   optional query params:
#     listing_type = 'sale' | 'rent'
#     emirate      = e.g. 'Dubai'
#     is_featured  = true | false
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[PropertyRead])
def get_all_properties(
    listing_type: Optional[Literal["sale", "rent"]] = Query(None),
    emirate:      Optional[str]                      = Query(None),
    is_featured:  Optional[bool]                     = Query(None),
    db:           Session                            = Depends(get_db),
):
    query = db.query(Property).filter(Property.is_active == True)

    if listing_type:
        query = query.filter(Property.listing_type == listing_type)
    if emirate:
        query = query.filter(Property.emirate.ilike(emirate))
    if is_featured is not None:
        query = query.filter(Property.is_featured == is_featured)

    return query.order_by(Property.id).all()


# ---------------------------------------------------------------------------
# GET /properties/{id}  –  return a single property
# ---------------------------------------------------------------------------
@router.get("/{property_id}", response_model=PropertyRead)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.is_active == True,
    ).first()

    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with id {property_id} not found.",
        )
    return prop


# ---------------------------------------------------------------------------
# POST /properties  –  create a new property listing
# ---------------------------------------------------------------------------
@router.post("/", response_model=PropertyRead, status_code=status.HTTP_201_CREATED)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    prop = Property(**payload.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop
