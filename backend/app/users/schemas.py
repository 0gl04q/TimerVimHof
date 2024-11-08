from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class SUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")


class SUserRegister(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(..., description="Email")
    username: str = Field(..., description="Username")
    password: str = Field(..., min_length=5, max_length=50, description="Password")


class SUserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=5, max_length=50, description="Password")
