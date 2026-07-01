from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, Developer
from app.schemas.schemas import DeveloperCreate, DeveloperRead, DeveloperUpdate

router = APIRouter(prefix="/developers", tags=["Developers"])


# ---------------------------------------------------------------------------
# GET /developers  –  public
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[DeveloperRead])
def get_all_developers(db: Session = Depends(get_db)):
    return (
        db.query(Developer)
        .filter(Developer.is_active == True)
        .order_by(Developer.sort_order, Developer.id)
        .all()
    )


# ---------------------------------------------------------------------------
# POST /developers  –  admin only
# ---------------------------------------------------------------------------
@router.post("/", response_model=DeveloperRead, status_code=status.HTTP_201_CREATED)
def create_developer(
    payload: DeveloperCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    dev = Developer(**payload.model_dump())
    db.add(dev)
    db.commit()
    db.refresh(dev)
    return dev


# ---------------------------------------------------------------------------
# PATCH /developers/{id}  –  admin only
# ---------------------------------------------------------------------------
@router.patch("/{developer_id}", response_model=DeveloperRead)
def update_developer(
    developer_id: int,
    payload: DeveloperUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(dev, field, value)
    db.commit()
    db.refresh(dev)
    return dev


# ---------------------------------------------------------------------------
# DELETE /developers/{id}  –  admin only
# ---------------------------------------------------------------------------
@router.delete("/{developer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_developer(
    developer_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found.")
    db.delete(dev)
    db.commit()
    return None