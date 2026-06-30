# New file for multiple images
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, Property, PropertyImage
from app.schemas.schemas import PropertyImageCreate, PropertyImageRead

router = APIRouter(prefix="/properties/{property_id}/images", tags=["Property Images"])


# ---------------------------------------------------------------------------
# GET /properties/{id}/images  –  public, list all images for a property
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[PropertyImageRead])
def get_property_images(property_id: int, db: Session = Depends(get_db)):
    return (
        db.query(PropertyImage)
        .filter(PropertyImage.property_id == property_id)
        .order_by(PropertyImage.sort_order)
        .all()
    )


# ---------------------------------------------------------------------------
# POST /properties/{id}/images  –  admin only, add one image
# ---------------------------------------------------------------------------
@router.post("/", response_model=PropertyImageRead, status_code=status.HTTP_201_CREATED)
def add_property_image(
    property_id: int,
    payload: PropertyImageCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found.")

    image = PropertyImage(
        property_id=property_id,
        image_url=payload.image_url,
        sort_order=payload.sort_order,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


# ---------------------------------------------------------------------------
# DELETE /properties/{id}/images/{image_id}  –  admin only
# ---------------------------------------------------------------------------
@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_image(
    property_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    image = db.query(PropertyImage).filter(
        PropertyImage.id == image_id,
        PropertyImage.property_id == property_id,
    ).first()

    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")

    db.delete(image)
    db.commit()
    return None

