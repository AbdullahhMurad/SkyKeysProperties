from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.models import AdminUser
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])

COOKIE_NAME = "access_token"
COOKIE_MAX_AGE = 60 * 60 * 8  # 8 hours, matches token expiry


@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(
        AdminUser.username == payload.username,
        AdminUser.is_active == True,
    ).first()

    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(data={"sub": admin.username, "role": admin.role})

    # httpOnly cookie — JS on the page can't read it, mitigates XSS token theft.
    # secure=True requires HTTPS, which Render provides in production.
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

    return {"status": "ok", "username": admin.username, "role": admin.role}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"status": "logged out"}