"""
FastAPI dependencies for authentication / RBAC.

Auth is cookie-based (httpOnly JWT) so it works seamlessly for both
the HTML admin panel and JSON API calls made from it.
"""
from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import AdminUser


def get_current_admin(
    request: Request,
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None),
) -> AdminUser:
    """
    Reads the JWT from the httpOnly cookie, validates it, and returns
    the matching active AdminUser. Raises 401 if anything is invalid.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_access_token(access_token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    username = payload["sub"]
    admin = db.query(AdminUser).filter(
        AdminUser.username == username,
        AdminUser.is_active == True,
    ).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found or disabled",
        )

    if admin.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )

    return admin


def get_current_admin_optional(
    request: Request,
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None),
) -> AdminUser | None:
    """
    Same as get_current_admin but returns None instead of raising.
    Used for HTML pages that need to know IF someone is logged in
    (e.g. to show/hide a nav link) without forcing a redirect.
    """
    if not access_token:
        return None
    payload = decode_access_token(access_token)
    if not payload or "sub" not in payload:
        return None
    return db.query(AdminUser).filter(
        AdminUser.username == payload["sub"],
        AdminUser.is_active == True,
    ).first()