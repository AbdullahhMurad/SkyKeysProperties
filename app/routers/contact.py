from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Enquiry

router = APIRouter(prefix="/api/contact", tags=["Contact"])


class ContactMessage(BaseModel):
    name:    str
    email:   Optional[str] = ""
    phone:   Optional[str] = ""
    subject: Optional[str] = "General Inquiry"
    message: str


@router.post("/")
def submit_contact(payload: ContactMessage, db: Session = Depends(get_db)):
    enquiry = Enquiry(
        full_name = payload.name,
        email     = payload.email or None,
        phone     = payload.phone or None,
        subject   = payload.subject or "General Inquiry",
        message   = payload.message,
    )
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return {"status": "saved", "id": enquiry.id}