from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminUserCreate(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)