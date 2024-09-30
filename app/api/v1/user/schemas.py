from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class UserM(BaseModel):
    """Main User model. Includes all data"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserCreateM(BaseModel):
    """User creates model"""
    username: str
    password: str

    @field_validator('username')
    def username_must_be_at_least_3_chars(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v

    @field_validator('password')
    def password_must_be_at_least_8_chars(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class TokenM(BaseModel):
    """Token model for OAuth"""
    access_token: str
    token_type: str
