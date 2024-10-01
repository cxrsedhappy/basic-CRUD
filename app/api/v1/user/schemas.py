from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field


# If you want to create BaseUser class wait until 3 or more classes needed.
class UserPublicM(BaseModel):
    """User **public** model. Includes only public data"""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="User name")
    created_at: datetime = Field(..., description="User creation time")
    updated_at: datetime = Field(..., description="User update time")

    class Config:
        from_attributes = True
        orm_mode = True


class UserPrivateM(BaseModel):
    """User **private** model. Includes private data"""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="User name")
    password: str = Field(..., description="User hashed password")
    created_at: datetime = Field(..., description="User creation time")
    updated_at: datetime = Field(..., description="User update time")

    class Config:
        from_attributes = True
        orm_mode = True


class UserPasswordChangeM(BaseModel):
    """User **private** model. Includes private data"""
    password: str = Field(min_length=8, max_length=32)


class UserCreateM(BaseModel):
    """User creates model"""
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=32)


class TokenM(BaseModel):
    """Token model for OAuth"""
    access_token: str
    token_type: str
