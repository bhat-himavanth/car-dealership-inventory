"""Request/response shapes (Pydantic).

These validate incoming JSON before it reaches our code, and control
exactly which fields go back out - e.g. a password hash never leaves the API.
"""
from pydantic import BaseModel, ConfigDict, Field


# ---------- Auth ----------

class UserCredentials(BaseModel):
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=255)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_admin: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Vehicles ----------

class VehicleCreate(BaseModel):
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(default=0, ge=0)


class VehicleUpdate(BaseModel):
    """All fields optional - only the ones sent get changed."""
    make: str | None = Field(default=None, min_length=1, max_length=100)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class VehicleOut(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RestockRequest(BaseModel):
    amount: int = Field(gt=0, le=1000)