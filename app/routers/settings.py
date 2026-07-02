from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, SiteSetting
from app.schemas.schemas import SiteSettingRead, SiteSettingUpdate

router = APIRouter(prefix="/settings", tags=["Site Settings"])


# ---------------------------------------------------------------------------
# GET /settings  –  public, returns all settings (templates use this)
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[SiteSettingRead])
def get_all_settings(db: Session = Depends(get_db)):
    return db.query(SiteSetting).all()


# ---------------------------------------------------------------------------
# PATCH /settings/{key}  –  admin only
# ---------------------------------------------------------------------------
@router.patch("/{key}", response_model=SiteSettingRead)
def update_setting(
    key: str,
    payload: SiteSettingUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Setting '{key}' not found.")

    setting.value = payload.value
    db.commit()
    db.refresh(setting)
    return setting