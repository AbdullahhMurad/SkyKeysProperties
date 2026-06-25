from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/contact", tags=["Contact"])


class ContactMessage(BaseModel):
    name:    str
    email:   str
    phone:   str = ""
    subject: str = "General Inquiry"
    message: str


@router.post("/")
def send_contact(payload: ContactMessage):
    # In production: send an email via SMTP / SendGrid / Mailgun here.
    # For now we log and return success so the form works end-to-end.
    print(f"[CONTACT] From: {payload.name} <{payload.email}>")
    print(f"[CONTACT] Subject: {payload.subject}")
    print(f"[CONTACT] Message: {payload.message}")
    return {"status": "received"}
