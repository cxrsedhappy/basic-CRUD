from pydantic import BaseModel, field_validator


class UserModel(BaseModel):
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
