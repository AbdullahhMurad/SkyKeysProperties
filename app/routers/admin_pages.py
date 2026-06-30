from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin_optional
from app.models.models import AdminUser

router = APIRouter(prefix="/admin", tags=["Admin Pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def admin_login_page(request: Request, db: Session = Depends(get_db)):
    # If already logged in, skip straight to dashboard
    current = get_current_admin_optional(request, db, request.cookies.get("access_token"))
    if current:
        return RedirectResponse(url="/admin/dashboard", status_code=302)

    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard_page(request: Request, db: Session = Depends(get_db)):
    current_admin = get_current_admin_optional(request, db, request.cookies.get("access_token"))
    if not current_admin:
        return RedirectResponse(url="/admin/login", status_code=302)

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "current_admin": current_admin,
    })