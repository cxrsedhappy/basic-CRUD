from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


# If you want to create BaseUser class wait until 3 or more classes needed.
class UserPublicM(BaseModel):
    """User **public** model. Includes only public data"""
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


class UserPrivateM(BaseModel):
    """User **private** model. Includes private data"""
    id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


class UserPasswordChangeM(BaseModel):
    """User **private** model. Includes private data"""
    password: str

    @field_validator('password')
    def password_must_be_at_least_8_chars(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


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
